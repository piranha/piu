run: .venv
	SECRET=epic-secret ./inve piud -p 3000 --path store -rd

.venv: setup.py requirements.txt
	test -d $@ || virtualenv --system-site-packages $@
	./inve python setup.py develop
	@touch $@
