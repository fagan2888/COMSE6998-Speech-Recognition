1. need [kaldi](https://github.com/kaldi-asr/kaldi) & [montreal forced aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases)
2. should create folders in root directory: `org_audio`, `segmented_audio`, `train-result`
3. run `bash pipeline-train.sh`
4. the model will be zip in `model.zip` in the root directory
5. run `bash pipeline-test.sh`

background music: [piano music played by Tim Shevlyakov](https://www.youtube.com/watch?v=kWUBmAMHd3M)

rock music: [Always there for you](https://archive.org/details/ClassicRockMusic80s90s/Always+there+for+you.mp3)

training set: [tedlium s5_r3](https://www.openslr.org/51/)

*note* kaldi-scp/*.scp come from `kaldi/egs/tedlium/s5_r3/data/train`, `kaldi/egs/tedlium/s5_r3/data/test`, and `kaldi/egs/tedlium/s5_r3/data/dev`

*note* only partial data (under `org_audio`, `segmented_audio`, `train-result` and `text`) are uploaded, please use run `kaldi/egs/tedlium/s5_r3/run.sh` to get the full dataset, and run `prepare_convert_to_wav.py` to convert wav from sph files