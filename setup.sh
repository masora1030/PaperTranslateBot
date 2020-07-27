mkdir downloads
cd downloads
sudo apt update
sudo apt upgrade -y
sudo apt install python3 python3-pip wkhtmltopdf
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt update
sudo apt -f install -y
sudo apt install python3-selenium
sudo apt install unzip
wget https://ipafont.ipa.go.jp/IPAexfont/IPAexfont00401.zip
unzip IPAexfont00401.zip -d ~/.fonts/
fc-cache -fv
pip3 install imgkit arxiv markdown
