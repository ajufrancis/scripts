<?php 
$nodeId = $_REQUEST["node"]; 
if($nodeId=="Home")
$res = '{
  "Root": [
  	{"Name": "Repository Home", 
	"ChildSubSet": [{
		 "id": "08bb3ddd-59d1-43f2-a7e2-fbe8caec60ad",
		 "text": "Folder1",
		 "path": "\/Repository Home",
		 "owner": "admin",
		 "isFolderLink": "true",
		 "isFolder": "true"
		 
	 }, {
		 "id": "08bb3dde-59d1-43f2-a7e2-fbe8caec60ad",
		 "text": "Folder2",
		 "path": "\/Repository Home",
		 "owner": "admin",
		 "isFolderLink": "false",
		 "isFolder": "true"
	 }, {
		 "id": "08bb3ddf-59d1-43f2-a7e2-fbe8caec60ad",
		 "text": "Folder3",
		 "path": "\/Repository Home",
		 "owner": "admin",
		 "isFolderLink": "true",
		 "isFolder": "true"
	 }, {
		 "id": "08bb3ddg-59d1-43f2-a7e2-fbe8caec60ad",
		 "text": "Folder4",
		 "path": "\/Repository Home",
		 "owner": "admin",
		 "isFolderLink": "false",
		 "isFolder": "true"
	 }, {
		 "id": "08bb3ddh-59d1-43f2-a7e2-fbe8caec60ad",
		 "text": "Folder5",
		 "path": "\/Repository Home",
		 "owner": "admin",
		 "isFolderLink": "false",
		 "isFolder": "true"
	 }],
	"isFolderLink":true
	}]
}';
else 
$res = '[{
			"id": "500c91ad-1a65-4467-843a-2ce46715e75d", 
			"text": "folder1",
			"path": "\/Company Home\/docs",
			"owner": "admin",
			"isFolderLink": "false",
		 	"isFolder": "true"
		}]';

echo $res;



?>

