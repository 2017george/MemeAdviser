import os
import app

test = os.getenv("test") not None
travis = os.getenv("HAS_JOSH_K_SEAL_OF_APPROVAL") not None

if travis:
	# travus sucks but whatever
	os.system("python -m pytest ./tests -v --cov=./src")
elif test and not travis:
	os.system("python3 -m pytest ./tests -v")
else:
	app.main()
