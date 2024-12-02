DEMO_URL = http://localhost:5000/benchmark/fibonacci/50?split=5&rounds=3000

cpu:
	curl http://localhost:5000/benchmark/fibonacci/cpu/10

io:
	curl http://localhost:5000/benchmark/fibonacci/io/10


build:
	@docker compose up  --build -d
	@sleep 5

demo:
	@echo $(DEMO_URL)
	@curl '$(DEMO_URL)&detail=0' | jq .


detail:
	@echo $(DEMO_URL)
	@curl '$(DEMO_URL)&detail=1' | jq .


test:
	@echo '$(DEMO_URL)&detail=0'
	@DEMO_URL='${DEMO_URL}&detail=0' k6 run load_test.js





