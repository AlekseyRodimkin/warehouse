dump:
	python app/manage.py dumpdata --indent 4 \
		--exclude auth.permission \
		--exclude contenttypes \
		--exclude admin.logentry \
		--exclude sessions \
		--exclude auth.user \
		auth.group warehouse > app/warehouse/fixtures/initial_data.json

migrate:
	python app/manage.py migrate

admin:
	python app/manage.py createsu

fix:
	python app/manage.py loaddata app/warehouse/fixtures/initial_data.json

run:
	python app/manage.py runserver