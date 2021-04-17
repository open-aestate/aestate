python delete.py
python setup.py sdist bdist_wheel
twine upload dist/*
git push origin main
git push gitee main