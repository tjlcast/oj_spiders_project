
create database bupt_oj_spider
	default character set utf8 ;

create table student_test_submit (
	id int primary key auto_increment,
	submit_id varchar(10),
	prob_id varchar(10),
	result varchar(10),
	memory varchar(10),
	code_language varchar(10),
	code_len varchar(10),
	submit_time varchar(10),
	user_name varchar(20),
	score varchar(10),
	evaluation_machine varchar(10),
	code varchar(300)
) ;
