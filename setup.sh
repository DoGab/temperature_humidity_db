#!/bin/bash

##---------------------------
## Version: 1.0.0
## Author: Dominic Gabriel
## Url: https://github.com/DoGab/thermvis
## --------------------------


##---------------------------
## ADJUSTABLE VARIABLES 
##---------------------------

INSTALLDIR=/opt/thermvis
USER=thermvis
GROUP=thermvis
GROUPID=10101
USERID=10101
PASSWORD=thermvis
USERHOME=/home/thermvis
USERSHELL=/bin/bash
USERDESC="Technical user for thermvis application"

##---------------------------
## STATIC VARIABLES 
##---------------------------

ADAFRUITGITHUBURL="https://github.com/adafruit/Adafruit_Python_DHT"
ADAFRUITINSTSCRIPT=setup.py

PREREQUISITE=git
INSTALLCMD="apt-get install -y"
GITCLONECMD="git clone"

SWDIR=$INSTALLDIR
BINDIR=$SWDIR/bin
CONFDIR=$SWDIR/etc
DBDIR=$SWDIR/db
LOGDIR=$SWDIR/log
ADADIR=$SWDIR/Adafruit_Python_DHT
DOCROOTDIR=/var/www/html

GITBINSCRIPT=sensor_to_db.py
GITBINDIR=bin
GITCONFDIR=etc
GITDOCROOT=var/www/html

SUDOERSDIR=/etc/sudoers.d
SUDOFILE=010_thermvis-nopasswd
SUDORULE="thermvis ALL=(ALL) NOPASSWD: /sbin/reboot, /usr/bin/python $BINDIR/$GITBINSCRIPT ???? ?"

DIRS=(
	"$SWDIR"
	"$BINDIR"
	"$CONFDIR"
	"$DBDIR"
	"$LOGDIR"
)

PACKAGESADA=(
	"build-essential"
	"python-dev"
)

PACKAGES=(
	"apache2"
	"git"
	"php7.0"
	"php-sqlite3"
	"libapache2-mod-php7.0"
	"sqlite3"
)

#verify copied files with md5sum?

##---------------------------
## FUNCTIONS
##---------------------------

source_os_release() {
	if [ -d /etc/os-release ]; then
		. /etc/os-release;
	fi
}

check_for_supported_os() {
	if [ ! $ID == 'raspian' ]; then
		echo "Operating system not supported";
		exit 1;
	else
		if [ ! $ID_VERSION == '8' ] && [ ! $ID_VERSION == '9' ]; then
			echo "Operating system version not supported";
			exit 1;
		fi
	fi
}

change_to_script_dir() {
	SCRIPTDIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
	cd $SCRIPTDIR;
}

create_directories() {
	for i in "${DIRS[@]}"
	do
		create_directory $i
	done
}

create_directory() {
	if [ ! -d $1 ]; then
		mkdir -p $1;
	fi
}

check_if_sw_installed() {
	command -v $1 >/dev/null 2>&1
	if [ $? -eq 1 ]; then
		echo >&2 "$1 not installed. Installing";
		install_package $1
		#exit 1;
	fi
}

check_for_git_dir() {
	if [ ! -d .git ]; then
		git rev-parse --git-dir 2> /dev/null;
		echo "Script must run in the git top directory";
		exit 1;
	fi
}

copy_files_from_to() {
	cp -R $SCRIPTDIR/$1/. $2/
}

install_sw_packages() {
	PKGS=$1
	for p in "${PKGS[@]}"
	do
		install_package $p
	done
}

install_package() {
	dpkg -l $p;
	if [ $? -eq 1 ]; then
		$INSTALLCMD $p
	fi
}

detect_document_root_dir() {
	#change to read the apache2 version
	case $ID_VERSION in
	'8')
		DOCROOTDIR=/var/www
		;;
	'9')
		DOCROOTDIR=/var/www/html
		;;
	esac
}

create_user_and_group() {
	# Check if user and group id are not used yet
	groupadd -g $GROUPID $GROUP
	useradd -c $USERDESC -d $USERHOME -g $GROUPID -m -u $USERID -p $PASSWORD -s $USERSHELL $USER
}

install_adafruit_sensor_lib() {
	RETURNCODE=$(curl -s --head $ADAFRUITGITHUBURL | head -n 1 | awk -F' ' '{ print $2}')
	echo $RETURNCODE
	if [ "$RETURNCODE" -eq 200 ]; then
		for p in "${PACKAGESADA[@]}"
		do
			echo "Install package: $p"
			install_package $p
		done
		create_directory $ADADIR
		$GITCLONECMD $ADAFRUITGITHUBURL.git $ADADIR
		cd $ADADIR
		if [ -f $ADAFRUITINSTSCRIPT ]; then
			python $ADAFRUITINSTSCRIPT install
		fi
		cd $SCRIPTDIR
#		rm -r $ADADIR
	fi
}

create_thermvis_sudo_rule() {
	if [ ! -f $SUDOERSDIR/$SUDOFILE ]; then
		echo "$SUDORULE" >> $SUDOERSDIR/$SUDOFILE
		chown root:root $SUDOERSDIR/$SUDOFILE
		chmod 600 $SUDOERSDIR/$SUDOFILE
	fi
}

set_owner_and_mode() {
	chown $USER:$GROUP $1
	chmod $2 $1
}

set_dir_permissions() {
	for dir in "${DIRS[@]}"
	do
		set_owner_and_mode $dir 755
	done
}

preparations_and_checks() {
	source_os_release
	check_for_supported_os
	check_if_sw_installed $PREREQUISITE
	change_to_script_dir
	check_for_git_dir
}

main() {
	preparations_and_checks
	
	create_user_and_group
	create_directories
	set_dir_permissions
	install_sw_packages $PACKAGES
	copy_files_from_to $GITBINDIR $BINDIR
	detect_document_root_dir
	copy_files_from_to $GITDOCROOT $DOCROOTDIR
	create_thermvis_sudo_rule
	install_adafruit_sensor_lib
	
}

##---------------------------
## MAIN
##---------------------------

main
