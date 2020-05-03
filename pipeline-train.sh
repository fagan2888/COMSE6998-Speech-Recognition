echo "[INFO] install python packages"
pip3 install -r python-requirements.txt

echo "[INFO] remove previous data"
rm -rf segmented_audio/*
rm -rf org_audio/*
rm -rf train-result/*
rm text
rm convert_to_wav.scp

echo "[INFO] prepare dataset"
python3 prepare_convert_to_wav.py
python3 prepare_data.py

echo "[INFO] train and align"
~/montreal-forced-aligner/bin/mfa_train_and_align ~/segmented_audio ~/kaldi/egs/tedlium/s5_r3/data/local/lang_nosp/align_lexicon.txt ~/train-result -c -v -o ~/model
echo "[INFO] model is trained"