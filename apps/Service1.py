from spyne import Iterable, Integer, Unicode, rpc, Application, ServiceBase, String
from spyne.protocol.http import HttpRpc
# from spyne.protocol.json import JsonDocument
from spyne.protocol.soap import Soap11

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
import dicttoxml
import datetime
import xmlschema
import xml.etree.ElementTree as ET

engine = create_engine('sqlite:///./database.db')

def getResultformDB(results):
    dictTemp = []
    for r in results:
        tempData={}
        tempData['room_no'] = r[0]
        tempData['time'] = r[1]
        tempData['temp'] = r[2]
        tempData['humidity'] = r[3]
        dictTemp.append(tempData)
    return dictTemp
    
class AirCondition(ServiceBase):
    
    @rpc(_returns=String)
    def getDataTest(ctx):
        string ="""
        <note>
            <to>Tove</to>
            <from>Jani</from>
            <heading>Reminder</heading>
            <body>Don't forget me this weekend!</body>
        </note>
        """
        return "test"
    
    @rpc(_returns=String)
    def getmydetail(ctx):
        tree = ET.parse('./apps/student.xml')
        root = tree.getroot()
        my_schema = xmlschema.XMLSchema('./apps/student.xsd')
        if(my_schema.is_valid(root)):
            return ET.tostring(root)
        else:
            return "<Error>Error NOT Valid</Error>"

    @rpc(_returns=String)
    def getDataDB(ctx):
        results = engine.execute('select * from aircondition')
        dictTemp = getResultformDB(results)
        xml = dicttoxml.dicttoxml(dictTemp)
        return xml

    @rpc(Unicode, _returns=String)
    def getDataFormRoom(ctx, room):
        results = engine.execute(f'select * from aircondition where room_no = {room}')
        dictTemp = getResultformDB(results)
        xml = dicttoxml.dicttoxml(dictTemp)
        return xml

    @rpc(Unicode, Unicode , _returns=String)
    def getDataDuration(ctx, dateStart, dateEnd):
        results = engine.execute(f"select * from aircondition where time >= '{dateStart}' and time <= '{dateEnd}'")
        dictTemp = getResultformDB(results)
        xml = dicttoxml.dicttoxml(dictTemp)
        return xml
    
    @rpc(Unicode, Unicode, Unicode,  _returns=String)
    def insertData(ctx, room, temp, humidity):
        results = engine.execute(
            f"INSERT INTO aircondition VALUES ('{room}', '{datetime.datetime.now()}', '{temp}', '{humidity}')"
            )
        
        return "<Result>Finish</Result>"


def getResultformDBkerry(results):
    dictTemp = []
    for r in results:
        tempData={}
        tempData['no_order'] = r[0]
        tempData['name'] = r[1]
        tempData['address'] = r[2]
        tempData['weight'] = r[3]
        tempData['status'] = r[4]
        dictTemp.append(tempData)
    return dictTemp

class KerryService(ServiceBase):
    # SELECT FUNCTION SQL
    @rpc(_returns=String)
    def getDataStored(ctx):
        results = engine.execute('SELECT * FROM kerrystored ORDER BY status ,no_order')
        dictTemp = getResultformDBkerry(results)
        xml = dicttoxml.dicttoxml(dictTemp)
        return xml

    @rpc(Unicode, _returns=String)
    def getlistname(ctx, name):
        results = engine.execute(f'SELECT * FROM kerrystored WHERE name = "{name}" ORDER BY status ,no_order')
        dictTemp = getResultformDBkerry(results)
        xml = dicttoxml.dicttoxml(dictTemp)
        return xml

    @rpc(Unicode, _returns=String)
    def getlistadd(ctx, address):
        results = engine.execute(f'SELECT * FROM kerrystored WHERE address = "{address}" ORDER BY status ,no_order')
        dictTemp = getResultformDBkerry(results)
        xml = dicttoxml.dicttoxml(dictTemp)
        return xml

    @rpc(Unicode, Unicode , _returns=String)
    def getlistweight(ctx, start, end):
        results = engine.execute(f"select * from kerrystored where weight >= '{start}' and weight <= '{end}' ORDER BY status ,no_order")
        dictTemp = getResultformDBkerry(results)
        xml = dicttoxml.dicttoxml(dictTemp)
        print(xml)
        return xml

    # INSERT FUNCTION SQL
    @rpc(Unicode, _returns=String)
    def insertSended(ctx, id_order):
        results = engine.execute(
            f"UPDATE kerrystored SET status = '1' WHERE no_order = {id_order}"
            )
        return "<Result>Finish insertSended</Result>"

    @rpc(Unicode, Unicode, Unicode,  _returns=String)
    def insertItem(ctx, name, address, weight):
        results = engine.execute(
            f"INSERT INTO kerrystored ('name','address','weight') VALUES ('{name}', '{address}', '{weight}')"
            )
        return "<Result>Finish insertItem</Result>"

def create_app(flask_app):
    """Creates SOAP services application and distribute Flask config into
    user con defined context for each method call.
    """
    application = Application([AirCondition,KerryService], 'spyne.examples.flask',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11(),
    )

    # Use `method_call` hook to pass flask config to each service method
    # context. But if you have any better ideas do it, make a pull request.
    # NOTE. I refuse idea to wrap each call into Flask application context
    # because in fact we inside Spyne app context, not the Flask one.

    # def _flask_config_context(ctx):
    #     ctx.udc = UserDefinedContext(flask_app.config)
    # application.event_manager.add_listener('method_call', _flask_config_context)

    return application