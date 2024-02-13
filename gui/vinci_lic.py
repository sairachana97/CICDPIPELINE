import os
import datetime
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
from pathlib import Path
from itertools import cycle

LICENSE_FILENAME = "vmlt.lic"
LICENSE_FOLDER = ".vmlt"
LICENSE_PASSPHRASE = "ml4cyber"
DATETIME_FORMAT = "%Y.%m.%d"
TOTAL_DAYS = 14
# change the date accordingly
START_DATE = "2022.01.27"


def _cryptBytes(data, key):
    if type(data) == str:
        return bytes(a ^ b for a, b in zip(bytes(data, "utf-8"), cycle(bytes(key,"utf-8"))))
    elif type(data) == bytes:
        return bytes(a ^ b for a, b in zip(data, cycle(key)))

def _createLicenseFile():
    today = datetime.datetime.now().strftime("%Y.%m.%d")
    licenseContents = "{0} {0} {1}".format(today, "1")
    licenseEncrypted = _cryptBytes(licenseContents, LICENSE_PASSPHRASE)
    licenseFolderPath = os.path.join(Path.home(), LICENSE_FOLDER)
    if not os.path.exists(licenseFolderPath):
        os.mkdir(licenseFolderPath)
    licensePath = os.path.join(licenseFolderPath, LICENSE_FILENAME)

    with open(licensePath, "wb") as f:
        f.write(licenseEncrypted)

    #License has been created
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Vinci ML Tool - Trial Information")
    msg.setText("Thank you for using Vinci ML Tool :).\nYour {} day trial started on {}.".format(TOTAL_DAYS, START_DATE))
    msg.exec_()

def _readLicenseFile():
    licensePath = os.path.join(Path.home(), LICENSE_FOLDER, LICENSE_FILENAME)
    with open(licensePath, "rb") as f:
        licenseEncrypted = f.read()
    licenseDecrypted = str(_cryptBytes(licenseEncrypted, bytes(LICENSE_PASSPHRASE, "utf-8")))
    if licenseDecrypted.startswith("b'") and licenseDecrypted.endswith("'"):
        licenseDecrypted = licenseDecrypted[2:-1]
    licenseDecrypted = licenseDecrypted.split(" ")
    installDateStr = licenseDecrypted[0]
    lastRunDateStr = licenseDecrypted[1]
    stillValidStr = licenseDecrypted[2]
    startDate = datetime.datetime.strptime(START_DATE, DATETIME_FORMAT)
    installDate = datetime.datetime.strptime(installDateStr, DATETIME_FORMAT)
    lastRunDate = datetime.datetime.strptime(lastRunDateStr, DATETIME_FORMAT)
    currentDate = datetime.datetime.now()

    timeEllapsed = currentDate - startDate
    timeEllapsedLastRun = currentDate - lastRunDate
    licenseValid = False

    if timeEllapsed.days > TOTAL_DAYS:
        #License has expired
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Vinci ML Tool - License Expired")
        msg.setText("Your {} day trial has expired by {} days.\nPlease renew your product :)\n\nVinci ML Tool will close.".format(TOTAL_DAYS,abs(TOTAL_DAYS - timeEllapsed.days)))
        msg.exec_()
        licenseValid = False
    elif timeEllapsed.days < 0:
        #Current date is less than start date.
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Vinci ML Tool - License Date Mismatch")
        msg.setText("Looks like you are using Vinci in the past.\nPlease renew your product :)\n\nVinci ML Tool will close.")
        msg.exec_()
        licenseValid = False
    elif timeEllapsedLastRun.days < -1:
        #Date was changed to extend license.
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Vinci ML Tool - License Altered")
        msg.setText("Looks like a date change was done on this PC.\nPlease renew your product :)\n\nVinci ML Tool will close.")
        msg.exec_()
        licenseValid = False
    elif stillValidStr == "0":
        #Date was changed to extend license.
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Vinci ML Tool - License not Vald")
        msg.setText("Current license is not valid anymore.\nPlease renew your product :)\n\nVinci ML Tool will close.")
        msg.exec_()
        licenseValid = False
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Vinci ML Tool - License Information")
        msg.setText("Your {} days license still has {} days left :)".format(TOTAL_DAYS, TOTAL_DAYS - timeEllapsed.days))
        msg.exec_()
        licenseValid = True
    
    today = datetime.datetime.now().strftime("%Y.%m.%d")
    licenseContents = "{0} {1} {2}".format(
            installDateStr, 
            today, 
            "1" if licenseValid else "0"
        )
    licenseEncrypted = _cryptBytes(licenseContents, LICENSE_PASSPHRASE)
    licenseFolderPath = os.path.join(Path.home(), LICENSE_FOLDER)
    if not os.path.exists(licenseFolderPath):
        os.mkdir(licenseFolderPath)
    licensePath = os.path.join(licenseFolderPath, LICENSE_FILENAME)

    with open(licensePath, "wb") as f:
        f.write(licenseEncrypted)

    return licenseValid and (stillValidStr == "1")


def _licenseFileExists():
    licensePath = os.path.join(Path.home(), LICENSE_FOLDER, LICENSE_FILENAME)
    return os.path.exists(licensePath)

def checkLicense():
    licenseValid = False
    if _licenseFileExists():
        #License file has already been created
        licenseValid = _readLicenseFile()
    else:
        #License file has not been created
        _createLicenseFile()
        licenseValid = True
    return licenseValid