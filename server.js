const express = require('express');
const fs = require('fs');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('templates')); // Serve arquivos da pasta templates

// Rota para autenticação
app.post('/login', (req, res) => {
    const { usuario, senha } = req.body;

    // Ler o arquivo de usuários
    fs.readFile('usuarios.txt', 'utf8', (err, data) => {
        if (err) {
            return res.status(500).send('Erro ao ler o arquivo de usuários.');
        }

        const usuarios = data.split('\n');
        let autenticado = false;

        for (let linha of usuarios) {            
            const [user, pass] = linha.split('|').map(item => item.trim());            
            if (user === usuario.trim() && pass === senha.trim()) {                
                autenticado = true;                
                break;            
            }
        }

        if (autenticado) {
            res.redirect('/main.html'); // Redirecionar para a página de sucesso
        } else {
            res.status(401).send('Usuário ou senha incorretos.');
        }
    });
});

// Rota para a página de login
app.get('/index.html', (req, res) => {
    res.sendFile(__dirname + '/templates/index.html'); // Corrigido para incluir o caminho correto
});

// Rota para a página principal
app.get('/main.html', (req, res) => {
    res.sendFile(__dirname + '/templates/main.html'); // Corrigido para incluir o caminho correto
});

// Iniciar o servidor
app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});