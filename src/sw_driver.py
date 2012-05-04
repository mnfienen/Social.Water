from social_water import *
import os
import base64

usr = '<MYACCOUNT>@gmail.com'


# the password is here encoded so that it can't be read by looking at this code. Not secure, but obfuscated
# to encode a password, in python, import base64 and set password to pwd
# then pwd_encoded = base64.b64encode(pwd)
# place the resulting string in place of '<ENCODED_PWD>' below
pwd_encoded = '<ENCODED_PWD>'
#email_scope dictates whether read all or just update using the following options:
#'ALL' means every message, 
#'UNSEEN' means just new unread ones
email_scope = 'UNSEEN'

print '############################'
print '#       Social.Water       #'
print '#    a m!ke@usgs joint     #'
print '############################'
print 'Making some initializations'
# get things rolling
# email_scope dictates whether read all or just update using the following options:
#'ALL' means every message, 
#'UNSEEN' means just new unread ones
allmsg = email_reader(usr,pwd_encoded,email_scope)

print 'Reading previous data from CSV files'
allmsg.read_CSV_data()



print 'Attempting to log on to gmail account'
# login to the account
allmsg.login()
print 'Succesfully logged on to gmail account'
# check the mail -- allmsg.checking_all_unseen 
# dictates whether read all or just update using the following options:
#'ALL' means every message, 
#'UNSEEN' means just new unread ones
print 'checking for messages'
allmsg.checkmail()

# make a quick check to see if any new messages. If there are not, quit without
# rewriting the charts and CSV files
if len(allmsg.msgids[0].split()) == 0:
    print 'No new messages: quitting now'
else:
    
    print 'parsing messages'
    # parse the messages
    allmsg.parsemail()
    print 'reading messages'
    # parse the individual messages
    allmsg.parsemsgs()
    
    # drop the data into a data fields
    print 'pushing data into fields'
    allmsg.update_data_fields()
    
    # write all data to CSV files
    print 'Writing data to CSV files'
    allmsg.write_all_data_to_CSV()
    
    # plot the results usung dygraphs
    print 'plot the results using dygraphs'
    allmsg.plot_results_dygraphs()
    
    
    
print '\nAll done for now!'
