now=$(date +"%Y-%m-%d %T")
echo "[INFO $now] preparing testset audioes"
python3 prepare_testset.py


now=$(date +"%Y-%m-%d %T")
echo "[INFO $now] aligning testing set"
~/montreal-forced-aligner/bin/mfa_align ~/testset-cleaned ~/kaldi/egs/tedlium/s5_r3/data/local/lang_nosp/align_lexicon.txt ~/test-result -c -v -j 8
now=$(date +"%Y-%m-%d %T")
echo "[INFO $now] successfully finished"