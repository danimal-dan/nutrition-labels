VENV_DIR ?= .venv

usage:       ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

install:     ## Install dependencies
	@which awslocal || pip install awscli-local
	test -e $(VENV_DIR) || virtualenv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate; pip install -r requirements.txt

run:         ## Deploy and invoke the Lambda container locally
	echo "Deploying Lambda locally"; \
	./build-and-deploy-localstack.sh; \
	echo "Done - test successfully finished."

start:
	EXTRA_CORS_ALLOWED_ORIGINS=http://localhost:5173 localstack start -d

stop:
	@echo
	localstack stop
ready:
	@echo Waiting on the LocalStack container...
	@localstack wait -t 30 && echo Localstack is ready to use! || (echo Gave up waiting on LocalStack, exiting. && exit 1)

logs:
	@localstack logs > logs.txt

test-ci:
	make start install ready run; return_code=`echo $$?`;\
	make logs; make stop; exit $$return_code;
	
.PHONY: usage install start run stop ready logs test-ci
