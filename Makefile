test:
	python ./encoder/wspr_signal.py
	./decoder/k9an-wsprd -f 10 wspr-i.wav
