echo 'Sync the REPO'
git pull
echo 'Copy Entire /app to outside'
cp -r /app /io
echo 'Check the arg value'
echo $1 >> filekey.key
echo 'RUN etl'
python update_package_names.py
echo 'Remove /io/app/data'
rm -rf /io/app/data
echo 'Copy /data Out'
cp -r data /io/app