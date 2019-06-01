DROP EXTENSION IF EXISTS pgcrypto;
CREATE EXTENSION pgcrypto;
/*
#Ref: https://dbtut.com/index.php/2018/10/01/column-level-encryption-with-pgcrypto-on-postgresql/
    #Encrypt: "PGP_SYM_ENCRYPT('The value to be entered in the column:','AES_KEY');
    #Decrypt: "PGP_SYM_DECRYPT(column_name::bytea,'AES_KEY');
*/

CREATE TABLE IF NOT EXISTS Users(id INT GENERATED ALWAYS AS IDENTITY,name VARCHAR,email VARCHAR,username VARCHAR,password VARCHAR,authToken VARCHAR);


DROP FUNCTION IF EXISTS spGetAllUsers;
CREATE FUNCTION spGetAllUsers()
RETURNS TABLE(ID INT,Name VARCHAR,Email VARCHAR,Username VARCHAR,Password VARCHAR(256)) AS $users$
	BEGIN
		RETURN QUERY SELECT U.id,U.name,U.email,U.username,U.password FROM Users U;
	END;
$users$ LANGUAGE plpgsql;

--select spGetAllUsers();

DROP FUNCTION IF EXISTS spLogin;
CREATE FUNCTION spLogin(usernameInput VARCHAR,passwordInput VARCHAR)
RETURNS BOOLEAN AS $$

	DECLARE
		usernameFound VARCHAR := (SELECT U.username FROM Users U WHERE U.username = usernameInput);
		decryptedPass VARCHAR := (SELECT PGP_SYM_DECRYPT(U.password::BYTEA,'AES_KEY') FROM Users U WHERE U.username = usernameInput);
	BEGIN
		
		IF usernameFound IS NOT NULL THEN
			IF (decryptedPass LIKE passwordInput) THEN
				RETURN TRUE;
			ELSE
				RETURN FALSE;
			END IF;
		ELSE
			BEGIN
				RETURN FALSE;
			END;
		END IF;
	END;
$$ LANGUAGE PLPGSQL;

--select * from spLogin('admin','admin');

DROP FUNCTION IF EXISTS spNewUser;
CREATE FUNCTION spNewUser(nameInput VARCHAR,emailInput VARCHAR,usernameInput VARCHAR,passwordInput VARCHAR)
RETURNS BOOLEAN AS $$
	DECLARE
		usernameFound VARCHAR(256) := (SELECT U.username FROM Users U WHERE U.username = usernameInput);
	BEGIN
		IF usernameFound IS NOT NULL THEN
			RETURN FALSE;
		ELSE
			INSERT INTO Users(name,email,username,password,authToken) VALUES(nameInput,emailInput,usernameInput,PGP_SYM_ENCRYPT(passwordInput,'AES_KEY'),'');
			RETURN TRUE;
		END IF;
		/*EXCEPTION WHEN OTHERS THEN
				RAISE EXCEPTION 'FAIL';
				ROLLBACK;*/
	END;
$$ LANGUAGE PLPGSQL;

--SELECT spNewUser('Feng','feng@correo.com','feng','feng');

/*
SELECT * FROM spNewUser('Administrador2','admi2n@correo.com','admin4','admin2');
*/

DROP FUNCTION IF EXISTS spSetAuthToken;

CREATE FUNCTION spSetAuthToken(usernameInput VARCHAR, tokenAutorizacionInput VARCHAR)
RETURNS BOOLEAN AS 
$$
	BEGIN
		DECLARE idCliente INT := (SELECT U.id FROM Users U where U.username = usernameInput);
		BEGIN
			IF idCliente IS NULL THEN
				RETURN FALSE;
			ELSE
				BEGIN
					UPDATE Users
						SET authToken = tokenAutorizacionInput WHERE idCliente = Users.id;
				END;
				RETURN TRUE;
			END IF;
		END;
	END;
$$
LANGUAGE PLPGSQL;

DROP FUNCTION IF EXISTS spGetAuthToken;

CREATE FUNCTION spGetAuthToken(usernameInput VARCHAR)
RETURNS VARCHAR AS 
$$
	BEGIN
		DECLARE idCliente INT := (SELECT U.id FROM Users U where U.username = usernameInput);
		BEGIN
			IF idCliente IS NULL THEN
				RETURN NULL;
			ELSE
				BEGIN
					RETURN (SELECT U.authToken FROM Users U WHERE U.id = idCliente);
				END;
			END IF;
		END;
	END;
$$
LANGUAGE PLPGSQL;

DROP FUNCTION IF EXISTS spMatchTokens;

CREATE FUNCTION spMatchTokens(usernameInput VARCHAR,tokenInput VARCHAR)
RETURNS BOOLEAN AS
$$
	BEGIN
		DECLARE idCliente INT := (SELECT U.id FROM Users U WHERE usernameInput = U.username);
		BEGIN
			IF idCliente IS NULL THEN
				RETURN FALSE;
			ELSE
				BEGIN
					IF (tokenInput LIKE (SELECT U.authToken FROM Users U WHERE U.id = idCliente)) THEN
						RETURN TRUE;
					ELSE
						RETURN FALSE;
					END IF; 
				END;
			END IF;
		END;
	END;
$$
LANGUAGE PLPGSQL;

insert into Users(name,email,username,password,authToken) VALUES ('Administrador','admin@correo.com','admin',PGP_SYM_ENCRYPT('admin','AES_KEY'),'token');

--select * from spGetAuthToken('feng');