from spyne import Iterable, Integer, Unicode, rpc, Application, ServiceBase, String
from spyne.protocol.http import HttpRpc
# from spyne.protocol.json import JsonDocument
from spyne.protocol.soap import Soap11

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
import dicttoxml

engine = create_engine('sqlite:///./database.db')

class AirCondition(ServiceBase):
    
    @rpc(_returns=String)
    def getData(ctx):
        string ="""
        <note>
            <to>Tove</to>
            <from>Jani</from>
            <heading>Reminder</heading>
            <body>Don't forget me this weekend!</body>
        </note>
        """
        return string

    @rpc(_returns=String)
    def getDataDB(ctx):
        results = engine.execute('select * from aircondition')
        dictTemp = []
        for r in results:
            tempData={}
            tempData['room_no'] = r[0]
            tempData['time'] = r[1]
            tempData['temp'] = r[2]
            tempData['humidity'] = r[3]
        
            dictTemp.append(tempData)
        xml = dicttoxml.dicttoxml(dictTemp)
        return xml

    @rpc(Integer, _returns=String)
    def getDataFormRoom(ctx, room):
        results = engine.execute(f'select * from aircondition where room_no = {room}')
        dictTemp = []
        for r in results:
            tempData={}
            tempData['room_no'] = r[0]
            tempData['time'] = r[1]
            tempData['temp'] = r[2]
            tempData['humidity'] = r[3]
        
            dictTemp.append(tempData)
        xml = dicttoxml.dicttoxml(dictTemp)
        return xml

    @rpc(Unicode,Unicode , _returns=String)
    def getDataDuration(ctx, dateStart, dateEnd):
        results = engine.execute(f"select * from aircondition where time >= '{dateStart}' and time <= '{dateEnd}'")
        dictTemp = []
        for r in results:
            tempData={}
            tempData['room_no'] = r[0]
            tempData['time'] = r[1]
            tempData['temp'] = r[2]
            tempData['humidity'] = r[3]
        
            dictTemp.append(tempData)
        xml = dicttoxml.dicttoxml(dictTemp)
        return xml
        
def create_app(flask_app):
    """Creates SOAP services application and distribute Flask config into
    user con defined context for each method call.
    """
    application = Application([AirCondition], 'spyne.examples.flask',
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