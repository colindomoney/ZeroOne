# Setting up Git-Crypt

This project uses [Git-Crypt](https://www.agwa.name/projects/git-crypt/) (and on [GitHub](https://github.com/AGWA/git-crypt)) to perform transparent encryption of secrets (SSH credentials) used in the project.

## Installing Git-Crypt

On Mac OS:
> brew install git-crypt

Installing from source:
> git clone https://www.agwa.name/git/git-crypt.git \
> cd git-crypt \
> make \
> make install

## Setting up Git-Crypt

If **and only if** you are setting up Git-Crypt for *the first time on a new repository* then you will need to initialise key storage as follows: 
> git-crypt init

There is an entry in the _.gitattributes_ file which specifies which files are to be processed by Git-Crypt as follows: 
```
secrets.yaml filter=git-crypt diff=git-crypt \
.gitattributes !filter !diff
```
These entries ensure that the _.gitattributes_ file itself it not encrypted, and the the file _secrets.yaml_ is filtered via Git-Crypt.

## Locking and Unlocking the Repository

Git-Crypt has two methods to encrypt files, the first uses GPG mode using keys distributed via GPG, and the second method uses symmetric encryption with a pre-shared key. The latter method is used to this project, please contact the author to get a copy of the key in Tar file format. 

Once you have the Tar file extract it to the route of your copy of the repository which should result in a file called _.key_. Once the respository has been checked out the _secretys.yaml_ file will be encrypted, in order to access the contents use the following command:

> git-crypt unlock .key

Once this command has been run the first time then Git will handle the encryption and decryption of the secrets transparently although it is also possible to explicitly use the _lock_ and _unlock_ commands.

## Accessing the SSH Credentials

Once the _secrets.yaml_ file has been decrypted a set of credentials will be revealed as follows:

```
ssh_credentials:
  - sshusername: "pi"
  - passphrase: "xxx"
  - ssh_private_key:
    "xxx"
```
The passphrase indicates the SSH command line password to be used when logging into the Raspberry Pi; however the preferred method is to use SSH authentication with the SSH private key provided. The private key is also _base64_ encoded so use the _base64_ command line utility to decode this and store the contents into a file, in my case called _id_rsa_zero-one_.

Finally add an entry to your SSH congig file to specify this file to be used for connections to the Pi either using a hostname or IP address, such as:

```
# cat ~/.ssh/config
Host rpi.local
        User pi
        IdentityFile /Users/colind/.ssh/id_rsa_zero-one
```