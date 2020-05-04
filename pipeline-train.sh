now=$(date +"%Y-%m-%d %T")
echo "[INFO $now] install python packages"
pip3 install -r python-requirements.txt

now=$(date +"%Y-%m-%d %T")
echo "[INFO $now] remove previous data"
rm -rf segmented_audio/*
rm -rf org_audio/*
rm -rf train-result/*
rm text
rm convert_to_wav.scp

now=$(date +"%Y-%m-%d %T")
echo "[INFO $now] prepare dataset"
python3 prepare_convert_to_wav.py
python3 prepare_data.py

now=$(date +"%Y-%m-%d %T")
echo "[INFO $now] train and align"
~/montreal-forced-aligner/bin/mfa_train_and_align ~/segmented_audio ~/kaldi/egs/tedlium/s5_r3/data/local/lang_nosp/align_lexicon.txt ~/train-result -c -v -o ~/model
now=$(date +"%Y-%m-%d %T")
echo "[INFO $now] model is trained"