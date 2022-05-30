import csv
import json
import sqlite3
 
def capitalisewords(string):
    list_of_words = string.split(" ")

    for word in list_of_words:
        list_of_words[list_of_words.index(word)] = word.capitalize()

    return " ".join(list_of_words)


def dictfactory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        # col[0] is the column name
        d[col[0]] = row[idx]
    return d


def createone(databasename, tablename):   
    createtable = f'''
    CREATE TABLE IF NOT EXISTS {tablename}
        (
            ID 'TEXT',
            Country TEXT,
            Brand TEXT,
            Type TEXT,
            Package TEXT,
            Rating TEXT
        )
    '''

    conn = sqlite3.connect(f'{databasename}.db')
    cur = conn.cursor()
    try:
        cur.execute(createtable)
        conn.commit()
        conn.close()
        print("Created table and file")
        return True
    except Exception as e:
        print(e)
        return False


def insertall(databasename, csvname):
    insertdata = f'''
    INSERT INTO {databasename}
        (
            ID,
            Country,
            Brand,
            Type,
            Package,
            Rating
        )
    VALUES(?, ?, ?, ?, ?, ?)
    '''
    data = []
    with open(f'{csvname}.csv','r',encoding='utf-8') as f:
        for x in csv.DictReader(f):
            data.append(x)

    conn = sqlite3.connect(f'{databasename}.db')
    cur = conn.cursor()
    
    for d in data:
        try:
            cur.execute(insertdata,(d['ID'],d['Country'],d['Brand'],d['Type'],d['Package'],d['Rating']))
            print(f'Inserted {d}')
        except Exception as e:
            print(e)
            return False
    conn.commit()
    conn.close()
    return True


def insertone(databasename, tablename, dic):
    insertkeys = ['ID','Country','Brand','Type','Package','Rating']
    columns = ()
    values = ()
    
    for key,value in dic.items():
        
        if key != 'ID':
            key = capitalisewords(key)

        if key not in insertkeys:
            print(f'{key} is a wrong column.')
        
        else:
            if key == 'Country':
                value = str(value.upper())
            elif key == 'Rating':
                value = str(value)
            elif key == 'ID':
                value = str(value)
            else:
                value = str(capitalisewords(value))
                
            values += (value,)
            columns += (key,)                                

    insertonerecord = f'''
    INSERT INTO {tablename} {columns}
    VALUES {values};
    '''
    
    conn = sqlite3.connect(f'{databasename}.db')
    cur = conn.cursor()
    cur.execute(insertonerecord)
    print(f'Inserted 1 record')
    conn.commit()
    conn.close()
    return True


def deleteall(databasename, tablename):
    deleteallrecords = f'''
    DELETE FROM {tablename}
    '''
    
    countrecords = f'''
    SELECT COUNT(*)
    FROM {tablename}
    '''
    
    conn = sqlite3.connect(f'{databasename}.db')
    cur = conn.cursor()
    count = cur.execute(countrecords).fetchone()[0]
    print(f'Deleting {count} records')
    cur.execute(deleteallrecords)
    print('All records deleted')
    conn.commit()
    conn.close()
    return True



def deletesome(databasename, tablename, dic):
    searchkeys = ['ID','Country','Brand','Type','Package','Rating']
    searchconditions = []
    
    for key,value in dic.items():
        if key != 'ID':
            key = capitalisewords(key)
            
        if key not in searchkeys:
            print(f'{key} is a wrong search condition.')
            continue
        
        else:
            if key == 'Country':
                value = value.upper()
            elif key == 'Rating':
                value = str(value)
            elif key == 'ID':
                value = str(value)
            else:
                value = capitalisewords(value)
                
            searchcondition = f'{key} = "{value}"'
            searchconditions.append(searchcondition)
            

    whereconditions = ' AND '.join(searchconditions)

    if whereconditions == '':
        print('Wrong search conditions given.')
        return False

    else:
        print(f'Search conditions: {whereconditions}')
        
        countrecords = f'''
        SELECT COUNT(*)
        FROM {tablename}
        WHERE {whereconditions}
        '''
        
        deletesomerecords = f'''
        DELETE FROM {tablename}
        WHERE {whereconditions}
        '''
        
        conn = sqlite3.connect(f'{databasename}.db')
        cur = conn.cursor()
        count = cur.execute(countrecords).fetchone()[0]
        print(f'Deleting {count} records')
        cur.execute(deletesomerecords)
        print('Some records deleted')
        conn.commit()
        conn.close()
        return True



def updatesome(databasename, tablename, dic):
    searchkeys = ['Country','Brand','Type','Package','Rating']
    updatekeys = ['Updatecountry','Updatebrand','Updatetype','Updatepackage','Updaterating']
    searchconditions = []
    updateconditions = []
    
    for key,value in dic.items():
        if key != 'ID':
            key = capitalisewords(key)

        if key not in searchkeys and key not in updatekeys:
            print(f'{key} is a wrong search condition.')
            continue
        
        else:
            #for search conditions
            if key in searchkeys:
                if key == 'Country':
                    value = value.upper()
                elif key == 'Rating':
                    value = float(value)
                else:
                    value = capitalisewords(value)
                    
                searchcondition = f'{key} = "{value}"'
                searchconditions.append(searchcondition)
                continue
            
            if key in updatekeys:
                if key == 'Updatecountry':
                    value = value.upper()
                elif key == 'Updaterating':
                    value = str(value)
                else:
                    value = capitalisewords(value)

                key = key.replace('Update', '', 1)
                updatecondition = f'{key} = "{value}"'
                updateconditions.append(updatecondition)
                    
            

    whereconditions = ' AND '.join(searchconditions)
    setconditions = ', '.join(updateconditions)

    if whereconditions == '':
        print('Wrong search conditions given.')
        return False

    else:
        print(f'Search conditions: {whereconditions}')
        print(f'Update conditions: {setconditions}')
        
        countrecords = f'''
        SELECT COUNT(*)
        FROM {tablename}
        WHERE {whereconditions}
        '''
        
        updatesomerecords = f'''        
        UPDATE {tablename}
        SET {setconditions}
        WHERE {whereconditions}
        '''

        conn = sqlite3.connect(f'{databasename}.db')
        cur = conn.cursor()
        count = cur.execute(countrecords).fetchone()[0]
        print(f'Updating {count} records')
        cur.execute(updatesomerecords)
        print('Some records updated')
        conn.commit()
        conn.close()
        return True



def searchsome(databasename, tablename, dic):
    searchkeys = ['ID','Country','Brand','Type','Package','Rating']
    searchconditions = []
    sortcondition = ''

    if 'Sortby' not in dic.keys() and 'sortby' not in dic.keys():
        print('No sort condition given.')
        return False
        
    else:
        
        for key,value in dic.items():
            if key != 'ID':
                key = capitalisewords(key)

            if key == 'Sortby':
                value = capitalisewords(value)
                
                if value.upper() == 'ID':
                    sortcondition += value.upper()
                elif value not in searchkeys:
                    print('Wrong sort condition given.')
                    return False
                else:
                    sortcondition += value
                continue

            if key == 'Keyword':
                value = capitalisewords(value)
                searchcondition = f"Type LIKE '%{value}%'"
                searchconditions.append(searchcondition)
                continue
                            
            if key not in searchkeys:
                print(f'{key} is a wrong search condition.')
                continue
            
            else:
                if key == 'Country':
                    value = value.upper()
                elif key == 'Rating':
                    value = str(value)
                elif key == 'ID':
                    value = str(value)
                else:
                    value = capitalisewords(value)
                    
                searchcondition = f"{key} = '{value}'"
                searchconditions.append(searchcondition)

    whereconditions = ' AND '.join(searchconditions)


    if whereconditions == '':
        print('Wrong search conditions given.')
        return False

    else:

        print(f'Search conditions: {whereconditions}')
        print(f'Sort conditions: {sortcondition}')

            
        countrecords = f'''
        SELECT COUNT(*)
        FROM {tablename}
        WHERE {whereconditions}
        '''

        searchsomerecords = f'''
        SELECT *
        FROM {tablename}
        WHERE {whereconditions}
        ORDER BY {sortcondition} ASC
        '''
        
        conn = sqlite3.connect(f'{databasename}.db')
        cur = conn.cursor()
        count = cur.execute(countrecords).fetchone()[0]
        print(f'Found {count} records')
        
        conn.row_factory = dictfactory
        cur = conn.cursor()
        records = cur.execute(searchsomerecords).fetchall()
        conn.commit()
        conn.close()
        return records #list of dicts


if __name__ == "__main__":
    createone('ratings','Ratings')
    insertall('ratings','ratings')
##    insertone('ratings','Ratings', {'brand':'Brand xxxx','country':'XXXX','ID':'2222222222222222'})
##    searchsome('ratings','Ratings', {'brand':'Brand A','country':'USA','Sortby':'country'})
##    searchsome('ratings','Ratings', {'country':'USA','sortby':'country','keyword':'instant'})
##    searchsome('ratings','Ratings', {'keyword':'seaweed','sortby':'id'})
##    updatesome('ratings','Ratings', {'brand':'Brand M','updatetype':'Hello world','updaterating':'0'})
##    deletesome('ratings','Ratings', {'country':'USA','package':'pack'})
##    deleteall('ratings','Ratings')    


