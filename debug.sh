echo 'Check the arg value'
echo $1
echo $2
echo 'Inside Container'
pip freeze
echo 'Check current directory'
ls
echo 'Check inside /app'
ls /app
echo 'Check inside /app/data'
ls /app/data
echo 'Check inside .git'
ls .git
echo 'Check size of /app/data'
du -sh /app/data
echo 'Checkout to main branch'
git checkout main
git pull
echo 'Check size of /app/data'
du -sh /app/data