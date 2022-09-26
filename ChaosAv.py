# _*_ coding:utf-8 _*_
"""markdown
* Author          : miho030(github)
* lastest update  : 25. 09. 2022
* file type : ChaosAv MainEngine Class
"""

import os
from EngineAPI import EngineInstance

# ---------------------------------  * * *  ---------------------------------
EngineInst = EngineInstance()

vecMalSize = []
vecParsedMalDB = []
vecBenignFileList = []
vecMalwareDB = \
[
    "68:44d88612fea8a8f36de82e1278abb02f:EICAR_TEST_FILE"
]
vecMalSig = \
[
    "X5O",
    "X5O!P%",
    "EICAR",
    "ANTIVIRUS-TEST-FILE!"
]

# ---------------------------------  * * *  ---------------------------------
class ChaosAv:
    def _Init(self):
        self.Malware_name = "EICAR_TEST_FILE"
        self.Malware_Desc = "Eicar antivirus test file"

        self._PrintUi()
        self._GetInfo()
        self._GetMalwareInfo()

        bRes = self._GetNTSystemDirList()
        if bRes == True:
            return True
        else:
            return False

    def _Uninit(self, bUninit):
        del self.Malware_name
        del self.Malware_Desc
        return 0


    def _PrintUi(self):
        """ test mode interface """
        print("+ =============================================== +")
        print("                 ChaosVc-Test-001                  ")
        print("                                     v0.0.0.1      ")
        print("                      *   *   *                    ")
        print("+ =============================================== +\n\n")

    def _GetInfo(self):
        SoftwareInfo = dict()
        SoftwareInfo["Author"] = "Aoi"
        SoftwareInfo["version"] = "0.0.0.1"
        SoftwareInfo["title"] = "EICAR Scan Engine"
        SoftwareInfo["miko_name"] = "eicar"
        SoftwareInfo["sig_num"] = 1

        return SoftwareInfo

    def _ShowEngineList(self):
        ScanEngineList = list()
        ScanEngineList.append("EICAR-Test-File (not a malware)")

        return ScanEngineList


    def _GetMalwareInfo(self):
        for strMalPattern in vecMalwareDB:
            strTmpMalData = strMalPattern.split(':')

            nTmpMalSize = int(strTmpMalData[0])
            if vecMalSize.count(nTmpMalSize) == 0:
                vecMalSize.append(nTmpMalSize)

            vecParsedMalDB.append(strTmpMalData[1])
            vecParsedMalDB.append(strTmpMalData[2])

    def __GetNTSystemFiles(self, strScanDirPath):
        try:
            vecScanFileList = []

            print("[DEBUG] ", "Caching directory data from system..")
            for (path, dir, files) in os.walk(strScanDirPath):
                print("\t-> [SUB-DEBUG] ", files)
                for strFileName in files:
                    strExt = os.path.splitext(strFileName)[-1]
                    vecScanFileList.append("%s\\%s" % (path, strFileName))
            print("[DEBUG] ", "Complete system Caching!")
            self._Scan(vecScanFileList)

            return vecScanFileList
        except IOError:
            pass

    def _GetNTSystemDirList(self):
        strScanDir = str(input("[+] Select your Directory which you want to scan(E.x : C://) : "))
        strfilteredScanDir = strScanDir.lstrip().rstrip()
        nSize = len(strfilteredScanDir)

        if nSize == 1:
            strTmpDir = strfilteredScanDir + ":\\"
            strDrivePath = os.path.abspath(strTmpDir)
            self.__GetNTSystemFiles(strDrivePath)

        elif nSize != 1:
            strDirPath = os.path.abspath(strfilteredScanDir)
            if os.path.isdir(strfilteredScanDir):
                self.__GetNTSystemFiles(strDirPath)
                return True
            else:
                return NotADirectoryError
        else:
            return False

    def _Scan(self, vecBenignFileList):
        try:
            if len(vecBenignFileList) != 0:
                bScanRes, vecScanRes, vecSafeRes = EngineInst._ScanEngine(vecParsedMalDB, int(vecMalSize[0]), vecMalSig, vecBenignFileList)

                if bScanRes == True:
                    self._Report(bScanRes, vecScanRes, vecSafeRes)
                else:
                    self._Report(bScanRes, vecScanRes, vecSafeRes)
            elif len(vecBenignFileList) == 0:
                nGetDirRes = self._GetNTSystemDirList()
                if nGetDirRes == False:
                    return FileNotFoundError
            else:
                return False
        except IOError:
            print("[DEBUG] ", " Failed module-_Scan engine")
            pass

    def _Report(self, nRes, vecDetectFileList, vecSafeFileList):
        if nRes == True:
            print("---------------------  Scan result  ---------------------")
            print("[+] ", "Total Scaned file count          : ", len(vecBenignFileList) + len(vecSafeFileList))
            print("[+] ", "Total of founded malware count   : ", len(vecDetectFileList))
            print("[+] ", "Total of Clean file count        : ", len(vecSafeFileList))
            print("\n * * * ")
            if len(vecDetectFileList) != 0:
                print("[+] ", "Detected malware informations ..")

                for strMalInfo in vecDetectFileList:
                    print("-------------------------------------------")
                    print("[MALWARE_NAME] ", strMalInfo[0])
                    print("\t Install directory : ", strMalInfo[1])
                self._Cure(0, vecDetectFileList)
            else:
                pass

        elif nRes == False:
            print("---------------------  Scan result  ---------------------")
            print("[ERROR] ", "System Error occured.")
            print("\tErrorCode -> ", "")

    def _Cure(self, nScanRes, vecToCureList):
        try:
            if nScanRes == 0:
                nCureRes = EngineInst.CureEngine(vecToCureList)
                if nCureRes == True:
                    return True
                else:
                    return False
        except IOError:
            pass
        return False


# ---------------------------------  * * *  ---------------------------------
def main():
    ChaosInst = ChaosAv()

    bIsInit = ChaosInst._Init()
    if bIsInit == False:
        ChaosInst._Uninit(bIsInit)

if __name__ == '__main__':
    main()
# ---------------------------------  * * *  ---------------------------------