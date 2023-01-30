TRUNCATE 
employee,
department,
contact,
client,
goods,
activity ,
transport_file
;
ALTER SEQUENCE employee_id_seq RESTART WITH 1;
ALTER SEQUENCE department_id_seq RESTART WITH 1;
ALTER SEQUENCE contact_id_seq RESTART WITH 1;
ALTER SEQUENCE client_id_seq RESTART WITH 1;
ALTER SEQUENCE good_id_seq RESTART WITH 1;
ALTER SEQUENCE activity_id_seq RESTART WITH 1;
ALTER SEQUENCE transport_file_id_seq RESTART WITH 1;