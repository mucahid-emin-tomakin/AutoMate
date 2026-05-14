@echo off
:: === Temporärer PATH ===
set "PATH=C:\Users\USER\Downloads\AutomationAnywhere\TTSFactory\MINICONDA\;C:\Users\USER\Downloads\AutomationAnywhere\TTSFactory\MINICONDA\Scripts;C:\Users\USER\Downloads\AutomationAnywhere\TTSFactory\MINICONDA\Library\bin;C:\Users\USER\Downloads\AutomationAnywhere\TTSFactory\FFMPEG\bin;%PATH%"
:: === Conda-Umgebung aktivieren ===
call "C:\Users\USER\Downloads\AutomationAnywhere\TTSFactory\MINICONDA\Scripts\activate.bat" AudioGenerator
:: === AudioGenerator ausführen ===
python "C:\Users\USER\Downloads\AutomationAnywhere\TTSFactory\TortoiseTTS\tortoise\AudioGenerator.py" ^
  --textfile "C:\Users\USER\Downloads\AutomationAnywhere\TTSFactory\AudioGeneratorText.txt" ^
  --text_split "80,200" ^
  --voice "Madara Uchiha" ^
  --output_path "C:\Users\USER\Downloads\AutomationAnywhere\TTSFactory\\" ^
  --output_name "AudioGenerator" ^
  --preset "high_quality" ^
  --candidates 1 ^
  --model_dir "C:\Users\USER\Downloads\AutomationAnywhere\TTSFactory\TortoiseTTS\tortoise\.cache\tortoise\models" ^
  --seed 1 ^
  --produce_debug_state false ^
  --use_deepspeed false ^
  --kv_cache true ^
  --half false ^
  --debug false ^
  --temperature 1 ^
  --length_penalty 1 ^
  --repetition_penalty 2 ^
  --top_p 1 ^
  --cond_free_k 2 ^
  --diffusion_temperature 1 ^
  --diffusion_iterations 444 ^
  --num_autoregressive_samples 333 ^
  --cond_free false 
exit
