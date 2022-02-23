expected1 = b"""<TimeSeries xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
	<series>
		<header>
			<type>instantaneous</type>
			<locationId>PS1313</locationId>
			<parameterId>h</parameterId>
			<qualifierId>mcc</qualifierId>
			<timeStep unit="nonequidistant" />
			<startDate date="2015-12-15" time="10:46:37" />
			<endDate date="2015-12-15" time="10:46:37" />
			<missVal>NaN</missVal>
			<sourceOrganisation>Mobile Water Management</sourceOrganisation>
			<sourceSystem>DEV</sourceSystem>
			<creationDate>2016-04-19</creationDate>
			<creationTime>22:11:17</creationTime>
		</header>
		<event comment="" date="2015-12-15" flag="1" flagSource="UR" time="10:46:37" value="-2.100" />
	</series>
</TimeSeries>"""

expected2 = b"""<ns0:TimeSeries xmlns:ns0="http://www.wldelft.nl/fews/PI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">\n  <ns0:series>\n    <ns0:header>\n      <ns0:type>instantaneous</ns0:type>\n      <ns0:locationId>PS2220</ns0:locationId>\n      <ns0:parameterId>h</ns0:parameterId>\n      <ns0:qualifierId>mcc</ns0:qualifierId>\n      <ns0:timeStep unit="nonequidistant" />\n      <ns0:startDate date="2021-06-01" time="15:00:39" />\n      <ns0:endDate date="2021-06-01" time="15:02:04" />\n      <ns0:missVal>-999</ns0:missVal>\n      <ns0:sourceOrganisation>Mobile Water Management</ns0:sourceOrganisation>\n      <ns0:sourceSystem>BES</ns0:sourceSystem>\n      <ns0:creationDate>2021-06-01</ns0:creationDate>\n      <ns0:creationTime>15:15:04</ns0:creationTime>\n    </ns0:header>\n    <ns0:event comment="" date="2021-06-01" flag="3" flagSource="UR" time="15:00:39" user="Aad Versteeg" value="-1.33" />\n    <ns0:event comment="" date="2021-06-01" flag="3" flagSource="UR" time="15:02:04" user="Aad Versteeg" value="-1.37" />\n  </ns0:series>\n</ns0:TimeSeries>"""
