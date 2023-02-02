*** Settings ***
Documentation	   API Testing in Robot Framework

Library			SeleniumLibrary
Library			RequestsLibrary
Library			JSONLibrary
Library			Collections
Library			OperatingSystem
Library			BuiltIn
Suite Setup		Create new session


*** Variables ***
# ${baseUrl}	https://logichainge-backend-github-26ar3gp3ja-ez.a.run.app.com
${baseUrl}	http://localhost
${Verify}	true
${Session}




*** Test Cases ***
Check for avalability on "/"
	[Documentation]	This test case verifies that the response code of the GET Request should be 200
	[Tags]	smoke
	${response}=	GET On Session	${Session}	/	expected_status=200

Try to upload json
	${json}=	Get File	test/robot/json/1.json
	${response}=	POST On Session	${Session}	/json/	data=${json}	expected_status=201

Check transport file has been added
	${response}=	GET On Session	${Session}	/transport_files/	expected_status=200
	${content}=	Set Variable	${response.json()}

	${content_length}=	Get Length	${content}
	Should Be Equal As Integers	${content_length}	1

	${id}=	Get Value From Json	${content[0]}	$.id
	Should Be Equal As Integers	${id[0]}	1

	${client_id}=	Get Value From Json	${content[0]}	$.client_id
	Should Be Equal As Integers	${client_id[0]}	1

*** Keywords ***
Create new session
	Create Session	${Session}	${baseUrl}	verify=${Verify}