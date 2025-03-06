SERVICE := circle-detection

build:
	docker compose build $(SERVICE)

run:
	docker compose run --rm $(SERVICE)

compile-requirements:
	docker compose run --rm $(SERVICE) sh -c "cd ../requirements && pip install pip-tools && pip-compile -U --resolver=backtracking"