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

Try to upload jsons
	${json}=	Get File	test/robot/json/1.json
	${response}=	POST On Session	${Session}	/json/	data=${json}	expected_status=201
	${json}=	Get File	test/robot/json/2.json
	${response}=	POST On Session	${Session}	/json/	data=${json}	expected_status=201

Check transport files have been added
	${response}=	GET On Session	${Session}	/transport_files/	expected_status=200
	${content}=	Set Variable	${response.json()}

	${content_length}=	Get Length	${content}
	Should Be Equal As Integers	${content_length}	2

Check the files were given default pending state
	${response}=	GET On Session	${Session}	/transport_files/get_by_status/pending	expected_status=200
	${content}=	Set Variable	${response.json()}

	${content_length}=	Get Length	${content}
	Should Be Equal As Integers	${content_length}	2

Check data for the first transport file
	${response}=	GET On Session	${Session}	/transport_files/1	expected_status=200
	${content}=	Set Variable	${response.json()}

	${id}=	Get Value From Json	${content}	$.id
	Should Be Equal As Integers	${id[0]}	1

	${client_id}=	Get Value From Json	${content}	$.client_id
	Should Be Equal As Integers	${client_id[0]}	1

*** Keywords ***
Create new session
	Create Session	${Session}	${baseUrl}	verify=${Verify}