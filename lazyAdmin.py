# Program to return default credentials based on searches made against specified json data containing credentials.
# The 2xdropout 2024
import json
import argparse

class File:
    def __init__(self, fileName = "./defaultCreds.json"):
        self.name = fileName
        self.json = ""
        self.brandList = []
        self.categoryList = []
    

    def BuildLists(self):
        for brands in self.json:
            self.brandList.append(str(brands.get('Brand')).upper())
            for categories in brands['Device Category']:
                self.categoryList.append(str(categories.get('Category Name')).upper())
        


    def ReadFile(self):

        with open(self.name, 'r') as file:
            self.json = json.load(file)
        file.close()

        self.BuildLists()

class UI:
    def __init__(self, filter, file):
        self.spacer = "==============================================="
        self.subSpacer = "\n********************************************"
        self.primaryKeys = ["Brand", "Category Name", "Credentials" ]
        self.filter = filter
        self.json = file.json
        self.sourceFile = file
    

    def DrawHeader(self):
        if(len(self.filter) < 2):
            infoString =f'''          {self.filter[0]}       '''
        else:
            infoString = f'''Brand:  {self.filter[0]}       Device:  {self.filter[1]}'''

        headerString = f'''
{infoString}
{self.spacer}
        '''

        print(headerString)


    def DumpJSON(self, raw = False):
        if(len(self.filter) > 1):
            for brands in self.json:
                if(str(self.filter[0]).upper() == str(brands.get('Brand')).upper()):
                    for categories in brands['Device Category']:
                        if(str(self.filter[1]).upper() == str(categories.get('Category Name')).upper()):
                            for key in categories['Credentials']:
                                print(f"USERNAME:  {key.get('Username')}        PASSWORD:  {key.get('Password')}")
                            for key in categories:
                                if(key in self.primaryKeys):
                                    continue
                                else:
                                    print(self.subSpacer)
                                    print(f"{key}:  {categories.get(key)}")
        else:
            if(self.filter[0] in self.sourceFile.brandList):
                for brands in self.json:
                    if(str(self.filter[0]).upper() == str(brands.get('Brand')).upper()):
                        for categories in brands['Device Category']:
                                print('\n', categories.get('Category Name'))
                                print(self.subSpacer.strip())
                                for key in categories['Credentials']:
                                    print(f"USERNAME:  {key.get('Username')}        PASSWORD:  {key.get('Password')}")
            else:
                for brands in self.json:
                    for categories in brands['Device Category']:
                        if(str(self.filter[0]).upper() == str(categories.get('Category Name')).upper()):
                                for key in categories['Credentials']:
                                    print(f"USERNAME:  {key.get('Username')}        PASSWORD:  {key.get('Password')}")
        
        print("\n"+self.spacer)



def main():
    sourceFile = File()

    msg = "lazyAdmin, a default credential tool by The  2xdropout"
    searchFilter = []

    parser = argparse.ArgumentParser(description = msg)
    parser.add_argument('-B', '--brand', help = 'Set device brand filter')
    parser.add_argument('-C', '--cat', help='Set device category')
    parser.add_argument('-b', '--listBrands', action = 'store_true', help = "List device brands")
    parser.add_argument('-c', '--listCats', action = 'store_true', help = 'List device categories')
    parser.add_argument('-F', '--fileName', help = 'Set json source data file name')

    args = parser.parse_args()

    if(args.fileName != None):
        sourceFile.name = args.fileName

    sourceFile.ReadFile()

    if(args.brand != None):
        keyString = str(args.brand).upper()
        if(keyString in sourceFile.brandList):
            searchFilter.append(keyString)
        else:
            print(f"Error:  {args.brand} not in brand list")
            exit()
    if(args.cat != None):
        keyString = str(args.cat).upper()
        if(keyString in sourceFile.categoryList):
            searchFilter.append(keyString)
        else:
            print(f"Error:  {args.cat} not in brand list")
            exit()
    if(args.listBrands != False):
        print("\nBRANDS:")
        print(set(sourceFile.brandList))
    if(args.listCats != False):
        print("\nCATEGORIES:")
        print(set(sourceFile.categoryList))
    
    if((args.brand != None) or (args.cat != None)):
        ui = UI(searchFilter, sourceFile)
        ui.DrawHeader()
        ui.DumpJSON()
    
    print('\n')

main()