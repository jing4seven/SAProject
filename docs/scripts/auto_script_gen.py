'''
auto_script_gen.py

This script only user for generate mysql initialize data in SAProject.
Please run it above django shell environment.
'''
from __future__ import unicode_literals
import xlrd
from datetime import datetime
import re
try:
    import django
except:
    raise Exception("Please run this script below django shell.")
    print "error"
else:
    del django

file_name = r'Permission.Design.xlsx'
script_file_name=r'mysql_init.sql'
role_list = []

def open_excel(file= 'file.xls'):
     try:
         data = xlrd.open_workbook(file)
         return data
     except Exception,e:
         print str(e)

def excel_table_byindex(file='file.xls',colnameindex=0,by_index=0):
     data = open_excel(file)
     table = data.sheets()[by_index]
     nrows = table.nrows
     ncols = table.ncols
     colnames =  table.row_values(colnameindex)
     list =[]
     for rownum in range(1,nrows):
          row = table.row_values(rownum)
          if row:
              app = {}
              for i in range(len(colnames)):
                 app[colnames[i]] = row[i]
              list.append(app)
     return list

def excel_table_byname(file= 'file.xls',colnameindex=0,by_name=u'Sheet1'):
     data = open_excel(file)
     table = data.sheet_by_name(by_name)
     nrows = table.nrows
     colnames =  table.row_values(colnameindex)
     list =[]
     for rownum in range(1,nrows):
          row = table.row_values(rownum)
          if row:
              app = {}
              for i in range(len(colnames)):
                 app[colnames[i]] = row[i]
              list.append(app)
     return list

def get_table_data(file='file.xlsx', colnameindex=0, by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows
    colnames = table.row_values(colnameindex)
    list = []

    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
    return list


def main():
    outputfile = open(script_file_name, 'w')

    # Script for Roles
    tables = excel_table_byname(file=file_name, colnameindex=1, by_name="Roles")
    outputfile.writelines('USE saproject\n')
    outputfile.writelines("# Roles\n")
    for row in tables:
        if re.match(r'^([A-Z| ]{2,8})$', row['Project Role']):
            #print 'INSERT INTO sa_t_role (`name`, enable, description) VALUES ("%s", True, "%s")' % (row['Project Role'], row['Description'])
            line_str = 'INSERT INTO sa_t_role (`name`, enable, description) VALUES ("%s", True, "%s");\n' % (row['Project Role'], row['Description'])
            outputfile.writelines(line_str)
            outputfile.writelines('SET @%s_pk=@@IDENTITY;\n' % row['Project Role'].replace(" ", "_"))
            role_list.append(row['Project Role'])

    #outputfile.writelines('GO\n')

    # Script for site_client
    outputfile.writelines('\n # Site Client\n')
    client_id = u'U11hRx68gSQkdhmEqo4YIGrrV8zJaCu3H5q3UKU17dI'
    security_key= u'VTExaFJ4NjhnU1FrZGhtRXFvNFlJR3JyVjh6SmFDdTNINXEzVUtVMTdkSQ'
    update_time = datetime.now()
    line_str = 'INSERT INTO sa_t_site_client (`name`, description, `client_id`, `security_key`, `scope`, `enable`,created_time) VALUES ("frontend", "That\'s a frontend", "%s", "%s", "all", True, "%s" );\n' % (client_id, security_key, update_time)
    outputfile.writelines(line_str)
    outputfile.writelines('SET @site_client_id=@@IDENTITY;\n')

    # Script for user
    outputfile.writelines('\n # Users\n')
    from django.conf import settings
    settings.configure()
    from django.contrib.auth import hashers
    users = ('userpo', 'userdev', 'userqa')
    raw_password = 'Pa88word'
    password = hashers.make_password(raw_password)
    update_time = datetime.now()
    last_login = datetime.now()
    date_joined = datetime.now()

    i=0
    for u in users:
        line_str = 'INSERT INTO sa_t_user (`username`,`password`, last_login, first_name, last_name, email, is_staff, is_active, date_joined, site_client_id, update_time, last_edited_by, birthday) VALUES ("%s", "%s", "%s", "%s", "XIAO", "test%s@test.com", False, True, "%s", @site_client_id, "%s", "admin", "1983-06-15T00:00");\n' % (u, password, last_login, u, i, date_joined, update_time)
        outputfile.writelines(line_str)
        outputfile.writelines('SET @%s_pk=@@IDENTITY;\n' % (u))
        i=i+1

    # Script for project
    outputfile.writelines('SELECT @userpo_pk=id FROM sa_t_user WHERE `username`="userpo";\n')
    line_str = 'INSERT INTO sa_t_projects (`name`, alias, owner_id, description, is_private, update_time, last_edited_by) VALUES ("ASPP", "A Sample Project Only For Test", @userpo_pk, "No Descriptions.",  False, "%s", "admin");\n' % (datetime.now())
    outputfile.writelines(line_str)
    outputfile.writelines('\nSET @project_pk=@@IDENTITY;\n')

    #outputfile.writelines('\nGO\n')

    # Script for Releases
    outputfile.writelines('\n# Releases\n')
    tables = excel_table_byname(file=file_name, colnameindex=0, by_name="Releases")
    for row in tables:
      line_str = 'INSERT INTO sa_t_releases (`name`, project_id, description, deadline, update_time, last_edited_by) '\
                 'VALUES ("%s", @project_pk, "%s", "%s",  "%s", "%s");\n' % (row["name"], row["description"], row["deadline"], datetime.now(), row["last_edited_by"])
      outputfile.writelines(line_str)
      outputfile.writelines('SET @release_pk=@@IDENTITY;\n')  

    # Script for WorkItemGroup
    outputfile.writelines('\n# WorkItemGroup\n')
    tables = excel_table_byname(file=file_name, colnameindex=0, by_name="WorkItemGroup")
    for row in tables:
      line_str = 'INSERT INTO sa_t_work_item_groups (project_id, `name`, description, importance, time_logged, initial_estimate, update_time, last_edited_by) '\
                 'VALUES (@project_pk, "%s", "%s", %s, %s, %s, "%s", "%s");\n' % (row["name"], row["description"], row["importance"], row["time_logged"], row["initial_estimate"], datetime.now(), row["last_edited_by"])
      outputfile.writelines(line_str)
      outputfile.writelines('SET @work_item_group_pk=@@IDENTITY;\n')  

    # Script for WorkItem
    outputfile.writelines('\n# WorkItem\n')
    tables = excel_table_byname(file=file_name, colnameindex=0, by_name="WorkItem")
    for row in tables:
      line_str = 'INSERT INTO sa_t_work_items (work_item_group_id, release_id, `name`, description, loe, creator_id, assignee_id, requestor_id, time_logged, update_time, last_edited_by) '\
                 'VALUES (@work_item_group_pk, @release_pk, "%s", "%s", %s, @userpo_pk, @userpo_pk, @userpo_pk, %s, "%s", "%s");\n' % (row["name"], row["description"], row["loe"], row["time_logged"], datetime.now(), row["last_edited_by"])
      outputfile.writelines(line_str)
      outputfile.writelines('SET @work_item=@@IDENTITY;\n')  

    # Script for project user role
    #outputfile.writelines('INSERT INTO sa_t_project_user_role (project_id, user_id, role_id) VALUES (@project_pk, @userpo_pk, @PO_pk);\n' )

    # Script for endpoint
    outputfile.writelines('\n# endpoint\n')
    tables = excel_table_byname(file=file_name, colnameindex=0, by_name="view.permissions")

    views_uri_dict = {}
    for row in tables:
        if row['Views'] and row['URI']:
            uri = row['URI'].split(' ')[-1].lower()
            if uri and not uri in views_uri_dict:
                   views_uri_dict[uri] = row['Views'].strip()
            #if uri:
                #outputfile.writelines('INSERT INTO sa_t_endpoint (`name`, codename) VALUES ("%s", "%s");\n' % (uri, row['Views'].strip()))

    for vu_k in views_uri_dict:
        outputfile.writelines('INSERT INTO sa_t_endpoint (`name`, codename) VALUES ("%s", "%s");\n' % (vu_k, views_uri_dict[vu_k]))

    # Script for permission
    act_dict = {'GET':0b1000, 'POST':0b0100, 'PUT':0b0010, 'DELETE':0b0001}
    perm_dict = {}
    for row in tables:
        if row['Views'] and row['URI']:
            act = row['URI'].split(' ')[0].upper()
            perm_uri = row['URI'].split(' ')[-1].lower()
            view_name = row['Views']
            perm_name = row['Project Permissions']
            roles = list(row['Roles'].split(','))
            temp_list= []
            temp_list.append(act_dict[act])
            temp_list.append(perm_uri)
            temp_list.append(view_name)
            temp_list.append(roles)
            perm_dict[perm_name] = temp_list
    outputfile.writelines("\n# permission\n")
    for perm_k in perm_dict:
        outputfile.writelines('SET @endpoint_pk=(SELECT id FROM sa_t_endpoint WHERE `name` = "%s" limit 1);\n' % (perm_dict[perm_k][1]))
        outputfile.writelines('INSERT INTO sa_t_permission (`name`, endpoint_id, GPPD) VALUES ("%s", @endpoint_pk, %d);\n' %(perm_k, perm_dict[perm_k][0] ))
        outputfile.writelines('SET @permission_pk=@@IDENTITY;\n')
        for r_name in perm_dict[perm_k][-1]:
            if r_name:
                outputfile.writelines('INSERT INTO sa_t_role_permission (role_id, permission_id) VALUES (@%s_pk, @permission_pk );\n' % (r_name.strip().replace(" ", "_")))
    #for perm_k in perm_dict:
        #print perm_dict[perm_k], perm_dict[perm_k][-1]
    # Script for project user role
    outputfile.writelines('\n # project user role\n')
    outputfile.writelines('INSERT INTO sa_t_project_user_role (project_id, role_id, user_id) VALUES (@project_pk, @PO_pk, @userpo_pk);\n' )
    outputfile.writelines('INSERT INTO sa_t_project_user_role (project_id, role_id, user_id) VALUES (@project_pk, @DEV_pk, @userdev_pk);\n')
    outputfile.writelines('INSERT INTO sa_t_project_user_role (project_id, role_id, user_id) VALUES (@project_pk, @QA_pk, @userqa_pk);\n' )

    outputfile.close()

if __name__=="__main__":
    main()
