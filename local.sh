clear
. ./venv/bin/activate
echo ""
echo ""
echo "                            Access the app at http://localhost:8000"
echo ""
echo ""
gunicorn app:app --bind 0.0.0.0:8000 --workers 2
