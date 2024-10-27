run:
	@cd server && uvicorn main:app --reload

gen-key:
	openssl rand -hex 32