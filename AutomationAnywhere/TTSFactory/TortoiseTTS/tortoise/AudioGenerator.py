#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AudioGenerator

# =========================================================================================================================================
#                                                               Imports & Setup
# =========================================================================================================================================

import warnings

warnings.filterwarnings("ignore")

import os

os.environ['HF_HOME'] = r"C:\Users\USER\Downloads\AutomationAnywhere\TTSFactory\TortoiseTTS\tortoise\.cache\huggingface"
os.environ['MODELS_DIR'] = r"C:\Users\USER\Downloads\AutomationAnywhere\TTSFactory\TortoiseTTS\tortoise\.cache\tortoise\models"

import sys
import time
import glob
import torch
import logging
import argparse
import subprocess
import torchaudio

from transformers import logging as hf_logging

hf_logging.set_verbosity_error()

from shutil import which
from api import TextToSpeech, MODELS_DIR
from utils.audio import load_audio, load_voices
from utils.text import split_and_recombine_text

# =========================================================================================================================================
#                                                        Hilfsfunktionen & Klassen
# =========================================================================================================================================

class LocalTextToSpeech(TextToSpeech):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = {
            'temperature': 0.8,
            'length_penalty': 1.0,
            'repetition_penalty': 2.0,
            'top_p': 0.8,
            'cond_free_k': 2.0,
            'diffusion_temperature': 1.0,
            'diffusion_iterations': 200
        }
        self.presets = {
            'ultra_fast': {
                'num_autoregressive_samples': 16,
                'diffusion_iterations': 30,
                'cond_free': False},
            'fast': {
                'num_autoregressive_samples': 96,
                'diffusion_iterations': 80},
            'standard': {
                'num_autoregressive_samples': 256,
                'diffusion_iterations': 200},
            'high_quality': {
                'num_autoregressive_samples': 333,
                'diffusion_iterations': 666,
                'diffusion_temperature': 1.0,
                'temperature': 0.85,
                'length_penalty': 1.1,
                'repetition_penalty': 2.0,
                'top_p': 0.95,
                'cond_free_k': 2.0,
                'cond_free': True
            },
        }

    def tts_with_preset(self, text, preset='high_quality', **kwargs):
        return super().tts_with_preset(text, preset, **kwargs)

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def log_header(title: str, width: int = 111):
    padding = max(0, (width - len(title) - 2) // 2)
    line = "=" * padding + f" {title} " + "=" * padding
    if len(line) < width:
        line += "="
    for handler in logger.handlers:
        original_formatter = handler.formatter
        handler.setFormatter(logging.Formatter('%(message)s'))
    logger.info(line)
    for handler in logger.handlers:
        handler.setFormatter(original_formatter)

def log_line(char: str = "=", width: int = 111):
    raw_line = char * width
    for handler in logger.handlers:
        original_formatter = handler.formatter
        handler.setFormatter(logging.Formatter('%(message)s'))
    logger.info(raw_line)
    for handler in logger.handlers:
        handler.setFormatter(original_formatter)

def get_ffmpeg_executable():    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))
    local_ffmpeg = os.path.join(base_dir, "FFMPEG", "bin", "ffmpeg.exe" if os.name == "nt" else "ffmpeg")

    if os.path.isfile(local_ffmpeg):
        return local_ffmpeg
    ffmpeg_path = which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    raise FileNotFoundError("Keine ffmpeg-Executable gefunden (weder lokal noch im Systempfad).")

# =========================================================================================================================================
#                                                               Hauptprogramm
# =========================================================================================================================================

if __name__ == '__main__':

    # ------------------------------------------------------
    #                 Argumente parsen
    # ------------------------------------------------------

    parser = argparse.ArgumentParser()
    parser.add_argument('--textfile',                   type=str,       default=None)
    parser.add_argument('--text_split',                 type=str,       default=None)
    parser.add_argument('--voice',                      type=str,       default=None)
    parser.add_argument('--output_path',                type=str,       default=None)
    parser.add_argument('--output_name',                type=str,       default=None)
    parser.add_argument('--preset',                     type=str,       default=None)
    parser.add_argument('--regenerate',                 type=str,       default=None)
    parser.add_argument('--candidates',                 type=int,       default=None)
    parser.add_argument('--model_dir',                  type=str,       default=MODELS_DIR)
    parser.add_argument('--seed',                       type=int,       default=None)
    parser.add_argument('--produce_debug_state',        type=str2bool,  default=None)
    parser.add_argument('--use_deepspeed',              type=str2bool,  default=None)
    parser.add_argument('--kv_cache',                   type=str2bool,  default=None)
    parser.add_argument('--half',                       type=str2bool,  default=None)
    parser.add_argument('--debug',                      type=str2bool,  default=None)
    parser.add_argument('--temperature',                type=float,     default=None)
    parser.add_argument('--length_penalty',             type=float,     default=None)
    parser.add_argument('--repetition_penalty',         type=float,     default=None)
    parser.add_argument('--top_p',                      type=float,     default=None)
    parser.add_argument('--cond_free_k',                type=float,     default=None)
    parser.add_argument('--diffusion_temperature',      type=float,     default=None)
    parser.add_argument('--diffusion_iterations',       type=int,       default=None)
    parser.add_argument('--num_autoregressive_samples', type=int,       default=None)
    parser.add_argument('--cond_free',                  type=str2bool,  default=None)
    args = parser.parse_args()

    # ------------------------------------------------------
    #            Logging Setup je nach Debug Flag
    # ------------------------------------------------------

    settings = None

    log_file = os.path.join(args.output_path, args.output_name + "Log.txt")

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)

    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    if args.debug:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")

    if device == "cuda":
        gpu_name = torch.cuda.get_device_name(0)
        gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    else:
        gpu_name = "N/A"
        gpu_mem = 0

    # ------------------------------------------------------
    #     CLI-Argumente → settings/presets überschreiben
    # ------------------------------------------------------

    tts = LocalTextToSpeech(models_dir=args.model_dir, use_deepspeed=args.use_deepspeed, kv_cache=args.kv_cache, half=args.half)

    preset_keys = set()
    for preset in tts.presets.values():
        preset_keys.update(preset.keys())

    if args.preset and args.preset in tts.presets:
        preset_values = tts.presets[args.preset]
        tts.settings.update({k: v for k, v in preset_values.items() if k in tts.settings})
    else:
        preset_values = {}

    for key in tts.settings.keys():
        val = getattr(args, key)
        if val is not None:
            tts.settings[key] = val

    for key in preset_keys:
        val = getattr(args, key)
        if val is not None:
            tts.presets[args.preset][key] = val

    # ------------------------------------------------------
    #                   Text laden und splitten
    # ------------------------------------------------------

    if not os.path.exists(args.textfile):
        logger.error(f"Textdatei nicht gefunden: {args.textfile}")
        sys.exit(1)

    with open(args.textfile, 'r', encoding='cp1252') as f:
        text = f.read().strip()

    if '|' in text:
        texts = text.split('|')
    elif args.text_split is not None:
        split_spec = args.text_split
        if ',' in split_spec:
            parts = split_spec.split(',')
            try:
                desired_len = int(parts[0])
                max_len = int(parts[1])
                texts = split_and_recombine_text(text, desired_len, max_len)
            except ValueError:
                logging.error(f"Ungültiges --text_split Format: {split_spec}. Erwartet: '80,200'")
                texts = split_and_recombine_text(text)
        elif split_spec.startswith('max:'):
            try:
                max_len = int(split_spec[4:])
                texts = split_and_recombine_text(text, 100, max_len)
            except ValueError:
                logging.error(f"Ungültige max: Angabe: {split_spec}")
                texts = split_and_recombine_text(text)
        else:
            logging.warning(f"Unbekanntes --text_split Format: {split_spec}. Verwende Standard.")
            texts = split_and_recombine_text(text)
    else:
        texts = split_and_recombine_text(text)

    # ------------------------------------------------------
    #               CUDA / DeepSpeed Einstellungen
    # ------------------------------------------------------

    if torch.backends.mps.is_available() and args.use_deepspeed:
        args.use_deepspeed = False
    if not torch.cuda.is_available() and not torch.backends.mps.is_available():
        logger.error("Weder CUDA noch MPS verfügbar!")
        sys.exit(1)

    status = "Done"
    flag_path = os.path.join(args.output_path, args.output_name + "Flag.txt")

    # ------------------------------------------------------
    #                  TTS Initialisierung
    # ------------------------------------------------------

    outpath = args.output_path
    outname = args.output_name
    selected_voices = args.voice.split(',')
    regenerate = None
    if args.regenerate:
        try:
            regenerate = [int(e.strip()) for e in args.regenerate.split(',') if e.strip().isdigit()]
        except Exception as e:
            logger.warning(f"Fehlerhafte Eingabe für --regenerate: {args.regenerate} – wird ignoriert.")
            regenerate = None
    seed = int(time.time()) if args.seed is None else args.seed
    torchaudio.set_audio_backend("soundfile")

    # ------------------------------------------------------
    #            Parameter & System Info ins Log
    # ------------------------------------------------------

    log_line("=", 111)
    log_header("SYSTEM-INFORMATIONEN", 111)
    log_line("=", 111)
    logger.info(f"Device/Amount: {device} / {torch.cuda.device_count()}")
    if torch.cuda.is_available():
        logger.info(f"GPU: {gpu_name} ({gpu_mem:.2f} GB VRAM)")
    else:
        logger.info("Keine CUDA GPU verfügbar – CPU oder MPS wird verwendet.")
    logger.info(f"PyTorch Version: {torch.__version__}")
    logger.info(f"MPS Available: {torch.backends.mps.is_available()}")
    logger.info(f"Flag-Datei: {os.path.join(args.output_path, args.output_name + 'Flag.txt')}")
    logger.info(f"Log-Datei: {log_file}")
    logger.info(f"HF_HOME: {os.environ['HF_HOME']}")

    log_line("=", 111)
    log_header("ROHDATEN AUS DER KOMMANDOZEILE ÜBERGEBENE ARGUMENTE (sys.argv)", 111)
    log_line("=", 111)
    logger.info(' '.join(sys.argv))

    log_line("=", 111)
    log_header("EINGEHENDE PARAMETER (args) (geparste)", 111)
    log_line("=", 111)
    for arg, val in vars(args).items():
        logger.info(f"{arg}: {val}")

    log_line("=", 111)
    log_header("INTERNE ABGELEITETE PARAMETER (Code erzeugt/berechnet)", 111)
    log_line("=", 111)
    logger.info(f"textfile: {args.textfile if args.textfile else 'Nicht gesetzt'}")
    logger.info(f"Anzahl der Textteile: {len(texts) if 'texts' in locals() and texts else 'Unbekannt'}")
    logger.info(f"voice: {args.voice if args.voice else 'Nicht gesetzt'}")
    logger.info(f"output_path: {args.output_path if args.output_path else 'Nicht gesetzt'}")
    logger.info(f"output_name: {args.output_name if args.output_name else 'Nicht gesetzt'}")
    logger.info(f"preset: {args.preset if args.preset else 'Nicht gesetzt'}")
    logger.info(f"regenerate: {args.regenerate if args.regenerate else 'Keine'}")
    logger.info(f"candidates: {args.candidates if args.candidates is not None else 'Nicht gesetzt'}")
    logger.info(f"model_dir: {args.model_dir if args.model_dir else 'Nicht gesetzt'}")
    logger.info(f"seed: {args.seed if args.seed is not None else 'Nicht gesetzt'}")
    logger.info(f"produce_debug_state: {args.produce_debug_state}")
    logger.info(f"use_deepspeed: {args.use_deepspeed}")
    logger.info(f"kv_cache: {args.kv_cache}")
    logger.info(f"half: {args.half}")
    logger.info(f"debug: {args.debug}")
    logger.info(f"temperature: {args.temperature}")
    logger.info(f"length_penalty: {args.length_penalty}")
    logger.info(f"repetition_penalty: {args.repetition_penalty}")
    logger.info(f"top_p: {args.top_p}")
    logger.info(f"cond_free_k: {args.cond_free_k}")
    logger.info(f"diffusion_temperature: {args.diffusion_temperature}")
    logger.info(f"diffusion_iterations: {args.diffusion_iterations}")
    logger.info(f"num_autoregressive_samples: {args.num_autoregressive_samples}")
    logger.info(f"cond_free: {args.cond_free}")
    logger.info(f"Device gewählt: {device if 'device' in locals() else 'Nicht definiert'}")

    if not text.strip():
        logging.error("Textdatei ist leer.")
        sys.exit(1)

    # ------------------------------------------------------
    #                   Hauptprozess
    # ------------------------------------------------------

    try:

        for selected_voice in selected_voices:
            voice_outpath = outpath 

            if '&' in selected_voice:
                voice_sel = selected_voice.split('&')
            else:
                voice_sel = [selected_voice]

            voice_samples, conditioning_latents = load_voices(voice_sel)
            all_parts = []
            for j, text in enumerate(texts):
                if regenerate is not None and j not in regenerate:
                    all_parts.append(load_audio(os.path.join(voice_outpath, f'{j}.wav'), 24000))
                    continue
                gen = tts.tts_with_preset(
                    text, 
                    voice_samples=voice_samples, 
                    conditioning_latents=conditioning_latents,
                    preset=args.preset,
                    k=args.candidates,
                    use_deterministic_seed=seed)

                if settings is None:
                    settings = tts.settings
                    log_line("=", 111)
                    log_header("API-PARAMETER (aus api.py)", 111)
                    log_line("=", 111)
                    if settings:
                        for key, value in settings.items():
                            logger.info(f"{key}: {value}")
                    else:
                        logger.warning("Keine API-Parameter verfügbar (settings ist None).")
                    log_line("=", 111)
                    log_header("Starte Generierung", 111)
                    log_line("=", 111)

                    logger.info(f"Wird geladen in: {voice_outpath, f'{j}.wav'}")

                if args.candidates == 1:
                    audio_ = gen.squeeze(0).cpu()
                    torchaudio.save(os.path.join(voice_outpath, f'{j}.wav'), audio_, 24000)
                else:
                    candidate_dir = os.path.join(voice_outpath, str(j))
                    os.makedirs(candidate_dir, exist_ok=True)
                    for k, g in enumerate(gen):
                        torchaudio.save(os.path.join(candidate_dir, f'{k}.wav'), g.squeeze(0).cpu(), 24000)
                    audio_ = gen[0].squeeze(0).cpu()
                all_parts.append(audio_)

            if args.candidates == 1:
                full_audio = torch.cat(all_parts, dim=-1)
                torchaudio.save(os.path.join(voice_outpath, f"{outname}.wav"), full_audio, 24000)

            if args.produce_debug_state:
                os.makedirs('debug_states', exist_ok=True)
                dbg_state = (seed, texts, voice_samples, conditioning_latents)
                torch.save(dbg_state, f'debug_states/read_debug_{selected_voice}.pth')

            if args.candidates > 1:
                audio_clips = []
                for candidate in range(args.candidates):
                    for line in range(len(texts)):
                        wav_file = os.path.join(voice_outpath, str(line), f"{candidate}.wav")
                        audio_clips.append(load_audio(wav_file, 24000))
                    audio_clips = torch.cat(audio_clips, dim=-1)
                    torchaudio.save(os.path.join(voice_outpath, f"{outname}_{candidate:02d}.wav"), audio_clips, 24000)
                    audio_clips = []

        # ------------------------------------------------------
        #                 FFMPEG WAV -> MP3
        # ------------------------------------------------------

        log_line("=", 111)
        log_header("WAV zu MP3 konvertieren mit ffmpeg", 111)
        log_line("=", 111)

        final_wav_path = os.path.join(outpath, f"{outname}.wav")

        max_wait_time = 333
        wait_interval = 1
        elapsed_time = 0
        while not os.path.exists(final_wav_path) and elapsed_time < max_wait_time:
            time.sleep(wait_interval)
            elapsed_time += wait_interval

        if not os.path.exists(final_wav_path):
            raise FileNotFoundError(f"Datei {final_wav_path} wurde nach {max_wait_time} Sekunden nicht gefunden.")

        final_mp3_path = os.path.splitext(final_wav_path)[0] + ".mp3"

        try:
            ffmpeg_exec = get_ffmpeg_executable()
            logger.info(f"ffmpeg verwendet: {ffmpeg_exec}")

            subprocess.run(
                [ffmpeg_exec, "-y", "-i", final_wav_path, final_mp3_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            logger.info(f"Erfolgreich in MP3 konvertiert: {final_mp3_path}")
        except FileNotFoundError:
            logger.error("ffmpeg wurde nicht gefunden. Bitte sicherstellen, dass es installiert und im PATH ist.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Fehler bei der MP3-Konvertierung: {e.stderr.decode()}")

        # ------------------------------------------------------
        #            WAV-Dateien im Ordner löschen
        # ------------------------------------------------------

        log_line("=", 111)
        log_header("Alle WAV-Dateien löschen", 111)
        log_line("=", 111)

        wav_files = glob.glob(os.path.join(voice_outpath, "*.wav"))
        for wav_file in wav_files:
            try:
                os.remove(wav_file)
                logger.info(f"WAV-Datei gelöscht: {wav_file}")
            except Exception as e:
                logger.error(f"Fehler beim Löschen von {wav_file}: {e}")

    except KeyboardInterrupt as e:
        status = f"Failed: User hat abgebrochen!"
        logger.error(f"Failed: User hat abgebrochen")
    except Exception as e:
        status = f"Failed: {e}"
        with open(flag_path, 'w', encoding='utf-8') as ef:
            ef.write(str(e))
        logger.error(f"Fehler: {e}")
    finally:
        with open(flag_path, 'w') as f:
            f.write(status.strip())
        logger.info(f"Flag-Datei geschrieben mit Status: {status}")
        log_line("=", 111)
        log_header("Generierung abgeschlossen", 111)
        log_line("=", 111)
