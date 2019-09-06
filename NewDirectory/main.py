# Copyright 2019 Daniel Zagorsky  , Web Developer Challange at Fast Simon.

import webapp2
HashMap = {}
NumEqualToHashMap = {}
UndoStackName = []
UndoStackValue = []
RedoStackName = []
RedoStackValue = []
CommandStack = []


#Average time complexity to remove/add/find in a dictionary is O(1).
class GetHandler(webapp2.RequestHandler):
    def get(self):

        # ---- Redo---- #
        CommandStack.append("get")
        # ---- Redo---- #

        # ---- Get---- #
        self.response.headers['Content-Type'] = 'text/plain'
        nameToGet = self.request.path_qs.split("=")[1]
        if HashMap.has_key(nameToGet) == False :
            self.response.write("None")
        else :
            variable_value = HashMap.get(nameToGet)
            self.response.write('%s' % variable_value)
        # ---- Get---- #




#Average time complexity to remove/add/find in a dictionary is O(1).
class SetHandler(webapp2.RequestHandler):
    def get(self):

        # ---- Redo---- #
        CommandStack.append("set")
        # ---- Redo----- #

        # ----- Set---- #
        self.response.headers['Content-Type'] = 'text/plain'
        ValueToSet = self.request.path_qs.split("value=")[1]
        NotCleanedNameToSet = self.request.path_qs.split("name=")[1]
        NameToSet = NotCleanedNameToSet.split("&value")[0]

        # ---- NUMEQUALTO----- #

        # One number increases , One to decreases
        if HashMap.has_key(NameToSet):

            ValTolvlUp = ValueToSet
            ValToReduce = HashMap.get(NameToSet)

            if NumEqualToHashMap.has_key(ValTolvlUp) == True:
                NumEqualToHashMap[ValTolvlUp] = int(NumEqualToHashMap.get(ValTolvlUp)) + 1
            if NumEqualToHashMap.has_key(ValTolvlUp) == False:
                NumEqualToHashMap[ValTolvlUp] = 1
            if NumEqualToHashMap.has_key(ValToReduce):
                if int(NumEqualToHashMap.get(ValToReduce)) > 0:
                    NumEqualToHashMap[ValToReduce] = int(NumEqualToHashMap.get(ValToReduce)) - 1

        # Only one number increases
        else:
            if NumEqualToHashMap.has_key(ValueToSet):
                NumEqualToHashMap[ValueToSet] = int(NumEqualToHashMap.get(ValueToSet)) + 1
            else:
                NumEqualToHashMap[ValueToSet] = 1

        # ---- NUMEQUALTO----- #



        HashMap[NameToSet] = ValueToSet
        # ----- Set----- #

        # ----- Undo---- #
        UndoStackName.append(NameToSet)
        UndoStackValue.append(ValueToSet)
        # ----- Undo----- #



        


        self.response.write('%s = %s' % (NameToSet, ValueToSet))




#Average time complexity to remove/add/find in a dictionary is O(1).
class UnsetHandler(webapp2.RequestHandler):
    def get(self):

        # ---- Redo----- #
        CommandStack.append("unset")
        # ---- Redo----- #

        self.response.headers['Content-Type'] = 'text/plain'

        # ----- Unset---- #
        NameToRemove = self.request.path_qs.split("=")[1]
        if HashMap.has_key(NameToRemove) == True:
            Value = HashMap.get(NameToRemove)

            # ---- NUMEQUALTO----- #
            if NumEqualToHashMap.has_key(Value):
                if NumEqualToHashMap.get(Value) > 0:
                    NumEqualToHashMap[Value] = NumEqualToHashMap.get(Value) - 1
            # ---- NUMEQUALTO----- #

            del HashMap[NameToRemove]
            # ----- Unset---- #

            # ----- Undo---- #
            UndoStackName.append(NameToRemove)
            UndoStackValue.append(None)
            # ----- Undo---- #


            self.response.write('%s = None' % NameToRemove)




#Clear is done by running over the array o(n)
class EndHandler(webapp2.RequestHandler):
    def get(self):

        # ---- End----- #
        self.response.headers['Content-Type'] = 'text/plain'
        HashMap.clear()
        NumEqualToHashMap.clear()
        del UndoStackName[:]
        del UndoStackValue[:]
        del RedoStackName[:]
        del RedoStackValue[:]
        del CommandStack[:]
        self.response.write('CLEANED')
        # ---- End----- #


#All actions are made on stack by append/pop at o(1) complexity
class UndoHandler(webapp2.RequestHandler):
    def get(self):

        CommandStack.append("undo")

        self.response.headers['Content-Type'] = 'text/plain'

        #Stack is empty
        if len(UndoStackName) == 0:
            self.response.write("NO COMMANDS")

        # Stack is Not empty
        else :

            TopName = UndoStackName.pop()

            # Only One Command
            if len(UndoStackName) == 0:

                 TopValue = UndoStackValue.pop()
                 if HashMap.has_key(TopName) == True:

                     del HashMap[TopName]

                     # ---- Redo----- #
                     RedoStackName.append(TopName)
                     RedoStackValue.append(TopValue)
                     # ---- Redo----- #


                     self.response.write('%s = None' % TopName)

            # More Than One Command
            else :

                SecondName = UndoStackName.pop()

                # Same Names , Update Value
                if TopName == SecondName :
                    TopValue = UndoStackValue.pop()
                    SecondValue = UndoStackValue.pop()
                    HashMap[SecondName] = SecondValue
                    UndoStackName.append(SecondName)
                    UndoStackValue.append(SecondValue)

                    # ---- Redo----- #
                    RedoStackName.append(TopName)
                    RedoStackValue.append(TopValue)
                    # ---- Redo----- #



                    self.response.write('%s = %s' % (SecondName, SecondValue))

                # Differennt Names , Remove Top name
                else :
                    TopValue = UndoStackValue.pop()
                    del HashMap[TopName]
                    UndoStackName.append(SecondName)

                    # ---- Redo----- #
                    RedoStackName.append(TopName)
                    RedoStackValue.append(TopValue)
                    # ---- Redo----- #


                    self.response.write('%s = None' % TopName)



#All actions are made on stack by append/pop at o(1) complexity
class RedoHandler(webapp2.RequestHandler):
    def get(self):

        #If another command was issued after an UNDO, the REDO command should do nothing.
        Command = CommandStack.pop()

        if Command != "undo" and  Command != "redo":

            CommandStack.append(Command)

        else :

            CommandStack.append("redo")


            self.response.headers['Content-Type'] = 'text/plain'

            # Stack is empty
            if len(RedoStackName) == 0:
                self.response.write("redooo")

            # Stack is Not empty
            else :

                TopName = RedoStackName.pop()
                TopValue = RedoStackValue.pop()

                # We need to Unset
                if TopValue == None:


                    del HashMap[TopName]

                    # ---- Undo----- #
                    UndoStackName.append(TopName)
                    UndoStackValue.append(TopValue)
                    # ---- Undo----- #

                    self.response.write('%s = None' % TopName)

                # We need to Set
                else :

                    HashMap[TopName] = TopValue

                    # ---- Undo----- #
                    UndoStackName.append(TopName)
                    UndoStackValue.append(TopValue)
                    # ---- Undo----- #

                    self.response.write('%s = %s' % (TopName, TopValue))



#Average time complexity to remove/add/find in a dictionary is O(1).
class NumEqualToHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        ValueToCheck = self.request.path_qs.split("value=")[1]

        if NumEqualToHashMap.has_key(ValueToCheck) == True:
            self.response.write("%s" % NumEqualToHashMap.get(ValueToCheck) )
        else :
            self.response.write("0")



app = webapp2.WSGIApplication([
   (r'/numequalto.*', NumEqualToHandler),
   ('/redo', RedoHandler),
   ('/undo', UndoHandler),
   ('/end', EndHandler),
   (r'/set.*', SetHandler),
   (r'/get\\?.*',GetHandler),
   (r'/unset.*', UnsetHandler),
   ], debug=False)



