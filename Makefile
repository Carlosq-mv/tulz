run:
	@cd server && uvicorn main:app --reload

dev:
	@cd client && npm run dev

gen-key:
	openssl rand -hex 32