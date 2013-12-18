rm -r output/
pelican content
sudo rsync -r -m -h --delete --progress output/ /srv/pycon-staging/
