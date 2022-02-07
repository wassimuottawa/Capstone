npx kill-port 5000
cd capstone-service
pip install -r requirements.txt
export FLASK_APP=api.py
python3 -m flask run
