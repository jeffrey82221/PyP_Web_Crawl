echo 'Check the arg value'
echo $1 >> filekey.key
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
echo 'Show git config'
git config --list
echo "Show remote branches:"
git branch -r
echo "Show remote branch URLs"
git remote -v
echo 'Check size of /app/data'
du -sh /app/data