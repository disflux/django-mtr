"""
This module provides an API for accessing the InterFAX web service.
"""

# Import our generated service stub classes.
from InterFax_services import *
from Inbound_services import *
import os
from util import deprecated
import datetime

from InterFax_services_types import *
QueryForm = ns0.QueryForm_Def(pname="QueryForm").pyclass
QueryCondition = ns0.QueryCondition_Def(pname="QueryCondition").pyclass
QueryControl = ns0.QueryControl_Def(pname="QueryControl").pyclass

class InterFaxClient:
    """
    This class provides access to the full InterFAX SOAP API.  Each API
    method is exposed as a method on this class.
    """

    def __init__(self,username,password):
        """
        Arguments:
        username - Your InterFAX username.
        password - Your InterFAX password.
        """
        
        if username is None:
            raise ValueError("Invalid username")
        self._username = username

        if password is None:
            raise ValueError("Invalid password")
        self._password = password

        # Build a proxy to the PostalMethods SOAP service.
        self._outboundProxy = InterFaxLocator().getInterFaxSoap()
        self._inboundProxy = InboundLocator().getInboundSoap()


    def sendCharFax(self,faxNumber,data,fileType="TXT"):
        """
        Makes a call to the InterFAX SendCharFax API method.
        see http://www.interfax.net/en/dev/webservice/reference/sendcharfax

        Arguments:
          faxNumber - The destination fax number in standard international 
                      notation e.g. +44-207-3456789
               data - Data of the document (text documents only)
           fileType - e.g. DOC, HTML, PS, etc. Default is TXT

        Returns: int
            In case of successful submission - the value contains the 
            TransactionID. In case of a failure, a negative value is returned.
            See the list of Web Service Return Codes:
            http://www.interfax.net/en/dev/webservice/reference/web-service-return-codes
        """
        # create a request
        req = SendCharFaxSoapIn()
        req._Password = self._password
        req._Username = self._username
        req._FaxNumber = faxNumber
        req._Data = data
        req._FileType = fileType
        result = self._outboundProxy.SendCharFax(req)._SendCharFaxResult
        return result


    def sendFax(self,faxNumber,filename):
        """
        Makes a call to the InterFAX SendFax API method.
        see http://www.interfax.net/en/dev/webservice/reference/sendfax

        Arguments:
          faxNumber - The destination fax number in standard international 
                      notation e.g. +44-207-3456789
           filename - The name of a local file to send (string).
                      see list of supported file types: 
                      http://www.interfax.net/en/help/supported_file_types

        Returns: int
            In case of successful submission - the value contains the 
            TransactionID. In case of a failure, a negative value is returned.
            See the list of Web Service Return Codes:
            http://www.interfax.net/en/dev/webservice/reference/web-service-return-codes
        """

        if not os.path.isfile(filename):
            raise ValueError("Invalid file: " + filename)
        ext = self._getExtension(filename)

        fileBytes = file(filename).read()

        # create a request
        req = SendfaxSoapIn()
        req._Password = self._password
        req._Username = self._username
        req._FaxNumber = faxNumber
        req._FileData = fileBytes
        req._FileType = ext
        result = self._outboundProxy.Sendfax(req)._SendfaxResult
        return result


    def sendFaxEx2(self,
                   faxNumbers,
                   contacts,
                   filenames,
                   postpone=None,
                   retries=3,
                   CSID=None,
                   pageHeader='N',
                   subject=None,
                   replyAddress=None,
                   pageSize=None,
                   pageOrientation=None,
                   isHighResolution=False,
                   isFineRendering=False ):
        """
        Makes a call to the InterFAX SendFaxEx_2 API method.
        see http://www.interfax.net/en/dev/webservice/reference/sendfaxex_2

        Arguments:
         faxNumbers - A list of fax numbers (strings).
           contacts - A list of contact names (strings). The entered string 
                      will appear: (1) for reference in the outbound queue, 
                      and (2) in the outbound fax header.
          filenames - A list of local filenames to send (string).
                      see list of supported file types:
                      http://www.interfax.net/en/help/supported_file_types
           postpone - Time to schedule the transmission. Defaults to ASAP.
            retries - Number of transmission attempts to perform, in case 
                      of fax transmission failure. Defaults to 3.
               CSID - Sender CSID (up to 20 characters). Defaults to user's 
                      default CSID.
         pageHeader - The fax header text to insert at the top of the page.
                      Defaults to no header.
            subject - Up to 60 characters, to be used as a reference only.
       replyAddress - An optional e-mail address to which feedback messages 
                      will be sent. Defaults to user's default reply address.
           pageSize - A4, Letter, Legal, or B4. Defaults to user's default
                      page size.
    pageOrientation - Portrait or Landscape. Defaults to user's default 
                      page orientation.
   isHighResolution - A boolean value. True ==> Fine, False ==> Standard. 
                      True renders documents more finely but takes longer to 
                      transmit (may therefore be more costly).
    isFineRendering - A boolean value. True ==> Optimize for greyscale, 
                      False ==> Optimize for B&W. "False" is recommended for 
                      textual, black & white documents, while "True" is better 
                      for greyscale text and for images.

        Returns: int
            In case of successful submission - the value contains the 
            TransactionID. In case of a failure, a negative value is returned.
            See the list of Web Service Return Codes:
            http://www.interfax.net/en/dev/webservice/reference/web-service-return-codes
        """

        bytes = b''

        fileTypes = []
        fileSizes = []
        for currFile in filenames:
            if not os.path.isfile(currFile):
                raise ValueError("Invalid file: " + currFile)
            fileTypes.append( self._getExtension(currFile) )
            currFileBytes = file(currFile).read()
            fileSizes.append( str( len(currFileBytes) ) )
            bytes = bytes + currFileBytes

        if None==postpone:
            postpone = datetime.datetime(1980, 1, 1)

        # create a request
        req = SendfaxEx_2SoapIn()
        req._Password = self._password
        req._Username = self._username
        req._FaxNumbers = ';'.join(faxNumbers)
        req._Contacts = ';'.join(contacts)
        req._FilesData = bytes
        req._FileTypes = ';'.join(fileTypes)
        req._FileSizes = ';'.join(fileSizes)
        req._Postpone = postpone.timetuple()
        req._RetriesToPerform = retries
        req._CSID = CSID,
        req._PageHeader = pageHeader
        req._Subject = subject
        req._ReplyAddress = replyAddress
        req._PageSize = pageSize
        req._PageOrientation = pageOrientation
        req._IsHighResolution = isHighResolution
        req._IsFineRendering = isFineRendering
        result = self._outboundProxy.SendfaxEx_2(req)._SendfaxEx_2Result
        return result


    def faxStatus(self,lastTransactionId,maxItems):
        """
        Makes a call to the InterFAX FaxStatus API method.
        see http://www.interfax.net/en/dev/webservice/reference/faxstatus

        Arguments:
        lastTransactionId - Only messages with TransactionID smaller than this 
                            parameter will be returned. 
                            For all transactions use 999999999
                 maxItems - Maximum number of FaxItem elements to be returned.

        Returns: a tuple of (resultCode, [] of FaxItem tuples)
                 resultCode of 0 means OK, negative number indicates an error.
                 See the list of Web Service Return Codes:
                 http://www.interfax.net/en/dev/webservice/reference/web-service-return-codes
                 Each FaxItem tuple is of the form
                 ( TransactionID,
                   SubmitTime,
                   PostponeTime,
                   CompletionTime,
                   DestinationFax,
                   RemoteCSID,
                   PagesSent,
                   Status,
                   Duration,
                   Subject,
                   PagesSubmitted )
        """

        # create a request
        req = FaxStatusSoapIn()
        req._Password = self._password
        req._Username = self._username
        req._LastTransactionID = lastTransactionId
        req._MaxItems = maxItems
        req._TotalCount = 10
        req._ListSize = 10
        req._ResultCode = 0

        returnVal = self._outboundProxy.FaxStatus(req)
        result = returnVal._FaxStatusResult

        returnVals = []
        if result._FaxItem:
            for currItem in result._FaxItem:
                print( dir(currItem) )
                returnVals.append( ( currItem._TransactionID,
                                     currItem._SubmitTime,
                                     currItem._PostponeTime,
                                     currItem._CompletionTime,
                                     currItem._DestinationFax,
                                     currItem._RemoteCSID,
                                     currItem._PagesSent,
                                     currItem._Status,
                                     currItem._Duration,
                                     currItem._Subject,
                                     currItem._PagesSubmitted ) )

        return ( returnVal._ResultCode, returnVals )


    def faxQuery(self,verb,verbData,maxItems):
        """
        Makes a call to the InterFAX FaxQuery API method.
        see http://www.interfax.net/en/dev/webservice/reference/faxquery

        Arguments:
            verb - PARENT <transactionid>; Retrieve ALL items in a batch
                   ACTIVE ; leave VerbData empty to retrieve ALL incomplete (active) items
                   GT <transactionid> transactions with id greater than the given transactionid
                   GE <transactionid> transactions with id greater than or equal to the given
                   transactionid
                   LT <transactionid> transactions with id smaller than the given transactionid
                   LE <transactionid> transactions with id smaller than or equal to the given
                   transactionid
                   EQ <transactionid> transactions with id equal to the given transactionid
                   BETWEEN <transactionid1,transactionid2> transactions with id greater than or equal to transactionid1 and id smaller than or equal to transactionid2.
                   IN <transactionid1,transactionid2> transactions in list. 
        verbData - Place <transactionid> required above here. See Verb.
        maxItems - Maximum number of FaxItem elements to be returned. Use -1 for no limit.

        Returns: a tuple of (resultCode, [] of FaxItemEx tuples)
                 resultCode of 0 means OK, negative number indicates an error.
                 See the list of Web Service Return Codes:
                 http://www.interfax.net/en/dev/webservice/reference/web-service-return-codes
                 Each FaxItemEx tuple is of the form
                 ( ParentTransactionID,
                   TransactionID,
                   SubmitTime,
                   PostponeTime,
                   CompletionTime,
                   UserID,
                   Contact,
                   JobID,
                   DestinationFax,
                   ReplyEmail,
                   RemoteCSID,
                   PagesSent,
                   Status,
                   Duration,
                   Subject,
                   PagesSubmitted,
                   SenderCSID,
                   Priority,
                   Units,
                   CostPerUnit,
                   PageSize,
                   PageOrientation,
                   PageResolution,
                   RenderingQuality,
                   PageHeader,
                   RetriesToPerform,
                   TrialsPerformed )
        """

        # create a request
        req = FaxQuerySoapIn()
        req._Password = self._password
        req._Username = self._username
        req._Verb = verb
        req._VerbData = verbData
        req._MaxItems = maxItems
        req._ResultCode = 0

        returnVal = self._outboundProxy.FaxQuery(req)
        result = returnVal._FaxQueryResult

        returnVals = []
        if result._FaxItemEx:
            for currItem in result._FaxItemEx:
                print( dir(currItem) )
                returnVals.append( ( currItem._ParentTransactionID,
                                     currItem._TransactionID,
                                     currItem._SubmitTime,
                                     currItem._PostponeTime,
                                     currItem._CompletionTime,
                                     currItem._UserID,
                                     currItem._Contact,
                                     currItem._JobID,
                                     currItem._DestinationFax,
                                     currItem._ReplyEmail,
                                     currItem._RemoteCSID,
                                     currItem._PagesSent,
                                     currItem._Status,
                                     currItem._Duration,
                                     currItem._Subject,
                                     currItem._PagesSubmitted,
                                     currItem._SenderCSID,
                                     currItem._Priority,
                                     currItem._Units,
                                     currItem._CostPerUnit,
                                     currItem._PageSize,
                                     currItem._PageOrientation,
                                     currItem._PageResolution,
                                     currItem._RenderingQuality,
                                     currItem._PageHeader,
                                     currItem._RetriesToPerform,
                                     currItem._TrialsPerformed ) )

        return ( returnVal._ResultCode, returnVals )


    def faxQuery2(self,queryForm,queryControl):
        """
        Makes a call to the InterFAX FaxQuery2 API method.
        see http://www.interfax.net/en/dev/webservice/reference/faxquery2

        Arguments:
           queryForm - A hash containing search criteria names as keys and
                       values that are either discrete values or 2-tuples of (verb,verbData).
                       These are the valid keys and sample values:
                                     Subject -> ( 'Equals', 'My Subject')
                                   FaxNumber -> ( 'Equals', '+12125554874' )
                                    DateFrom -> a datetime.datetime.timetuple() instance
                                      DateTo -> a datetime.datetime.timetuple() instance
                                      UserId -> ( 'Equals', '101' )
                                ReplyAddress -> ( 'Like', '%Main Street%' )
                               TransactionId -> ( 'LessThan', '999999999' )
                         ParentTransactionId -> ( 'GreaterThan, '123456789' )
                                      Status -> ('Equals', 0)
                       ShowHiddenTransaction -> False

                       For full documentation see: http://www.interfax.net/en/dev/webservice/reference/faxquery2

        queryControl - A hash containing variables that control how the results are
                       built and returned.
                       These are the valid keys and sample values:

                             OnlyParents -> False
                            NumOfResults -> 10
                          StartingRecord -> 0
                                 OrderBy -> 'TransactionID'
                       AscOrderDirection -> True
                             ReturnItems -> True
                             ReturnStats -> False

                       For full documentation see: http://www.interfax.net/en/dev/webservice/reference/faxquery2

        Returns: a tuple of (resultCode, [] of FaxItemEx tuples)
                 resultCode of 0 means OK, negative number indicates an error.
                 See the list of Web Service Return Codes:
                 http://www.interfax.net/en/dev/webservice/reference/web-service-return-codes
                 Each FaxItemEx tuple is of the form
                 ( ParentTransactionId,
                   TransactionId,
                   SubmitTime,
                   PostponeTime,
                   CompletionTime,
                   UserId,
                   Contact,
                   JobID,
                   DestinationFax,
                   ReplyEmail,
                   RemoteCSID,
                   PagesSent,
                   Status,
                   Duration,
                   Subject,
                   PagesSubmitted,
                   SenderCSID,
                   Priority,
                   Units,
                   CostPerUnit,
                   PageSize,
                   PageOrientation,
                   PageResolution,
                   RenderingQuality,
                   PageHeader,
                   RetriesToPerform,
                   TrialsPerformed )
        """

        # create a request
        queryFormArg = self._buildQueryForm( queryForm )
        queryControlArg = self._buildQueryControl( queryControl )

        req = FaxQuery2SoapIn()
        req._Password = self._password
        req._Username = self._username
        req._QueryForm = queryFormArg
        req._QueryControl = queryControlArg

        returnVal = self._outboundProxy.FaxQuery2(req)
        result = returnVal._FaxQuery2Result

        returnVals = []

        if result._FaxItems:
            for currItem in result._FaxItems._FaxItemEx2:
                print( dir(currItem) )
                returnVals.append( ( currItem._ParentTransactionID,
                                     currItem._TransactionID,
                                     currItem._SubmitTime,
                                     currItem._PostponeTime,
                                     currItem._CompletionTime,
                                     currItem._UserID,
                                     currItem._Contact,
                                     currItem._JobID,
                                     currItem._DestinationFax,
                                     currItem._ReplyEmail,
                                     currItem._RemoteCSID,
                                     currItem._PagesSent,
                                     currItem._Status,
                                     currItem._Duration,
                                     currItem._Subject,
                                     currItem._PagesSubmitted,
                                     currItem._SenderCSID,
                                     currItem._Priority,
                                     currItem._Units,
                                     currItem._CostPerUnit,
                                     currItem._PageSize,
                                     currItem._PageOrientation,
                                     currItem._PageResolution,
                                     currItem._RenderingQuality,
                                     currItem._PageHeader,
                                     currItem._RetriesToPerform,
                                     currItem._TrialsPerformed ) )

        return ( result._ResultCode, returnVals )


    def getFaxImage(self,transactionId,outfilename):
        """
        Makes a call to the InterFAX GetFaxImage API method.
        see http://www.interfax.net/en/dev/webservice/reference/getfaximage

        Arguments:
        transactionId - Id of the fax transaction to fetch.
          outfilename - Name of a local file to write the result to.

        Returns: If retrieval of fax image is successful, return value is 0.
                 In case of failure, a negative value is returned.
                 See the list of Web Service Return Codes:
                 http://www.interfax.net/en/dev/webservice/reference/web-service-return-codes
        """

        # create a request
        req = GetFaxImageSoapIn()
        req._Password = self._password
        req._Username = self._username
        req._TransactionID = transactionId

        result = self._outboundProxy.GetFaxImage(req)
        if 0==result._GetFaxImageResult:
            outfile = open(outfilename,"wb")
            outfile.write(result._Image)
            outfile.close()

        return result._GetFaxImageResult


    def reSendFax(self,transactionId,faxNumber):
        """
        Makes a call to the InterFAX ReSendFax API method.
        see http://www.interfax.net/en/dev/webservice/reference/resendfax

        Arguments:
        transactionId - Id of the fax transaction to resend.
            faxNumber - The destination fax number to which to resend this 
                        transaction, in standard international notation
                        e.g. +44-207-3456789

        Returns: int
            In case of successful submission - the value contains the 
            TransactionID. In case of a failure, a negative value is returned.
            See the list of Web Service Return Codes:
            http://www.interfax.net/en/dev/webservice/reference/web-service-return-codes
        """

        # create a request
        req = ReSendFaxSoapIn()
        req._Password = self._password
        req._Username = self._username
        req._TransactionID = transactionId
        req._FaxNumber = faxNumber

        result = self._outboundProxy.ReSendFax(req)
        return result._ReSendFaxResult


    def hideFax(self,transactionId):
        """
        Makes a call to the InterFAX HideFax API method.
        see http://www.interfax.net/en/dev/webservice/reference/hidefax

        Arguments:
        transactionId - TransactionID of transaction to hide from outbound queue.

        Returns: 
          resultCode of 0 means OK, negative number indicates an error.
          See the list of Web Service Return Codes:
          http://www.interfax.net/en/dev/webservice/reference/web-service-return-codes
        """

        # create a request
        req = HideFaxSoapIn()
        req._Password = self._password
        req._Username = self._username
        req._TransactionID = transactionId

        result = self._outboundProxy.HideFax(req)
        return result._HideFaxResult


    def cancelFax(self,transactionId):
        """
        Makes a call to the InterFAX CancelFax API method.
        see http://www.interfax.net/en/dev/webservice/reference/cancelfax

        Arguments:
        transactionId - TransactionID of transaction to hide from outbound queue.

        Returns: 
          resultCode of 0 means OK, negative number indicates an error.
          See the list of Web Service Return Codes:
          http://www.interfax.net/en/dev/webservice/reference/web-service-return-codes
        """

        # create a request
        req = CancelFaxSoapIn()
        req._Password = self._password
        req._Username = self._username
        req._TransactionID = transactionId

        result = self._outboundProxy.CancelFax(req)
        return result._CancelFaxResult


    def getList(self,listType,maxItems):
        """
        Makes a call to the InterFAX GetList API method to return a list of
        received faxes.
        see http://www.interfax.net/en/dev/webservice/reference/getlist

        Arguments:
             listType - One of: AllMessages, NewMessages, AccountAllMessages, AccountNewMessages
             maxItems - Maximum items to return, between 1 to 100

        Returns: a tuple of (resultCode, [] of MessageItem tuples)
                 resultCode of 0 means OK, negative number indicates an error.
                 See the list of Web Service Return Codes:
                 http://www.interfax.net/en/dev/webservice/reference/web-service-return-codes
                 Each MessageItem tuple is of the form
                 ( MessageID,
                   PhoneNumber,
                   RemoteCSID
                   MessageStatus
                   Pages
                   MessageSize
                   MessageType
                   ReceiveTime
                   CallerID
                   MessageRecordingDuration )
        """

        req = GetListSoapIn()
        req._Password = self._password
        req._Username = self._username
        req._LType = listType
        req._MaxItems = maxItems

        result = self._inboundProxy.GetList(req)

        returnVals = []

        if result._objMessageItem:
            for currItem in result._objMessageItem._MessageItem:
                print( dir(currItem) )
                returnVals.append( ( currItem._MessageID,
                                     currItem._PhoneNumber,
                                     currItem._RemoteCSID,
                                     currItem._MessageStatus,
                                     currItem._Pages,
                                     currItem._MessageSize,
                                     currItem._MessageType,
                                     currItem._ReceiveTime,
                                     currItem._CallerID,
                                     currItem._MessageRecordingDuration ) )

        return ( result._GetListResult, returnVals )


    def getImageChunk(self,messageId,markAsRead,chunkSize,readFrom,outfilename):
        """
        Makes a call to the InterFAX GetImageChunk API method.
        see http://www.interfax.net/en/dev/webservice/reference/getimagechunk

        Arguments:
            messageId - Message ID of the transaction to download.
           markAsRead - True - mark as read. False - doesn't change the current status.
            chunkSize - Buffer size to download.
             readFrom - Starting point of the image to write to the buffer
          outfilename - Name of a local file to write the result to.

        Returns: If retrieval of fax image is successful, return value is 0.
                 In case of failure, a negative value is returned.
                 See the list of Web Service Return Codes:
                 http://www.interfax.net/en/dev/webservice/reference/web-service-return-codes
        """

        # create a request
        req = GetImageChunkSoapIn()
        req._Password = self._password
        req._Username = self._username
        req._MessageID = messageId
        req._MarkAsRead = markAsRead
        req._ChunkSize = chunkSize
        req._From = readFrom

        result = self._inboundProxy.GetImageChunk(req)

        print dir(result)

        if 0==result._GetImageChunkResult:
            outfile = open(outfilename,"wb")
            outfile.write(result._Image)
            outfile.close()

        return result._GetImageChunkResult


    ####

    def _buildQueryForm( self, queryForm ):

        result = QueryForm()

        dontCare = self._buildQueryCond( 'Equals', None )

        if queryForm.has_key('Subject'):
            s = queryForm['Subject']
            result._Subject = self._buildQueryCond( s[0], s[1] )
        else:
            result._Subject = dontCare
            print "Subject"

        if queryForm.has_key('FaxNumber'):
            s = queryForm['FaxNumber']
            result._FaxNumber = self._buildQueryCond( s[0], s[1] )
        else:
            result._FaxNumber = dontCare
            print "FaxNumber"

        if queryForm.has_key('DateFrom'):
            result._DateFrom = queryForm['DateFrom']
        else:
            # Default is a date sufficiently in the past to catch everything.
            result._DateFrom = datetime.datetime(1980,1,1,0,0,0).timetuple()

        if queryForm.has_key('DateTo'):
            result._DateTo = queryForm['DateTo']
        else:
            # Default is now
            result._DateTo = datetime.datetime.now().timetuple()
        
        if queryForm.has_key('UserId'):
            s = queryForm['UserId']
            result._UserID = self._buildQueryCond( s[0], s[1] )
        else:
            result._UserID = dontCare

        if queryForm.has_key('ReplyAddress'):
            s = queryForm['ReplyAddress']
            result._ReplyAddress = self._buildQueryCond( s[0], s[1] )
        else:
            result._ReplyAddress = dontCare

        if queryForm.has_key('TransactionId'):
            s = queryForm['TransactionId']
            result._TransactionID = self._buildQueryCond( s[0], s[1] )
        else:
            result._TransactionID = dontCare

        if queryForm.has_key('ParentTransactionId'):
            s = queryForm['ParentTransactionId']
            result._ParentTransactionID = self._buildQueryCond( s[0], s[1] )
        else:
            result._ParentTransactionID = dontCare

        if queryForm.has_key('Status'):
            s = queryForm['Status']
            result._Status = self._buildQueryCond( s[0], s[1] )
        else:
            result._Status = dontCare

        if queryForm.has_key('ShowHiddenTransactions'):
            result._ShowHiddenTransactions = queryForm['Status']
        else:
            result._ShowHiddenTransactions = False

        return result


    def _buildQueryControl( self, queryControl ):


        result = QueryControl()

        if queryControl.has_key('OnlyParents'):
            result._OnlyParents = queryControl['OnlyParents']
        else:
            result._OnlyParents = False

        if queryControl.has_key('NumOfResults'):
            result._NumOfResults = queryControl['NumOfResults']
        else:
            result._NumOfResults = 10

        if queryControl.has_key('StartingRecord'):
            result._StartingRecord = queryControl['StartingRecord']
        else:
            result._StartingRecord = 0

        if queryControl.has_key('OrderBy'):
            result._OrderBy = queryControl['OrderBy']
        else:
            result._OrderBy = 'TransactionID'

        if queryControl.has_key('AscOrderDirection'):
            result._AscOrderDirection = queryControl['AscOrderDirection']
        else:
            result._AscOrderDirection = True

        if queryControl.has_key('ReturnItems'):
            result._ReturnItems = queryControl['ReturnItems']
        else:
            result._ReturnItems = True

        if queryControl.has_key('ReturnStats'):
            result._ReturnStats = queryControl['ReturnStats']
        else:
            result._ReturnStats = False

        return result


    def _buildQueryCond(self, verb, verbData ):
        res = QueryCondition()
        res._Verb = verb
        res._VerbData = verbData
        return res


    def _getExtension(self,filename):
        if not filename:
            raise ValueError('invalid filename')
        basename = os.path.basename(filename)
        ext = os.path.splitext(basename)[1]
        if not ext:
            raise ValueError("File has no extension: " + filename)
        ext = ext.strip('.').upper()
        return ext
