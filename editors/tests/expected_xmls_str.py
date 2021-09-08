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
		<event comment="" date="2015-12-15" flag="1" flagsource="UR" time="10:46:37" value="-2.100" />
	</series>
</TimeSeries>"""
expected2 = b"""<TimeSeries xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xsi:schemaLocation="http://www.wldelft.nl/fews/PI http://fews.wldelft.nl/schemas/version1.0/pi-schemas/pi_timeseries.xsd">
  <series>
    <header>
      <type>instantaneous</type>
      <locationId>PS2220</locationId>
      <parameterId>h</parameterId>
      <qualifierId>mcc</qualifierId>
      <timeStep unit="nonequidistant" />
      <startDate date="2021-06-01" time="15:00:39" />
      <endDate date="2021-06-01" time="15:02:04" />
      <missVal>-999</missVal>
      <sourceOrganisation>Mobile Water Management</sourceOrganisation>
      <sourceSystem>BES</sourceSystem>
      <creationDate>2021-06-01</creationDate>
      <creationTime>15:15:04</creationTime>
    </header>
    <event comment="" date="2021-06-01" flag="3" flagsource="UR" time="15:00:39" user="Aad Versteeg" value="-1.33" />
    <event comment="" date="2021-06-01" flag="3" flagsource="UR" time="15:02:04" user="Aad Versteeg" value="-1.37" />
  </series>
</TimeSeries>"""
