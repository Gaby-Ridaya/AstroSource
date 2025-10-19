import { useEffect, useState } from 'react';

function UserFilesList({ user }) {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchFiles() {
      setLoading(true);
      setError('');
      try {
        const response = await fetch('/api/files');
        if (!response.ok) throw new Error('Erreur API: ' + response.status);
        const data = await response.json();
        // Nouvelle API : data.files est un tableau
        if (data && Array.isArray(data.files)) {
          if (user) {
            // Filtrer les fichiers pour l'utilisateur
            setFiles(data.files.filter(f => f.user === user));
          } else {
            setFiles(data.files);
          }
        } else {
          setFiles([]);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchFiles();
  }, [user]);

  if (loading) return <div>Chargement des fichiers...</div>;
  if (error) return <div style={{color:'red'}}>Erreur : {error}</div>;
  if (!files || files.length === 0) return <div>Aucun fichier trouvé.</div>;

  return (
    <div>
      <h3>Fichiers générés {user ? `pour ${user}` : 'pour tous les utilisateurs'}</h3>
      <ul>
        {files.map((file, idx) => (
          <li key={idx}>
            <strong>{file.user ? file.user + ' : ' : ''}</strong>
            <span>{file.name}</span>
            {file.path && (
              <a href={file.path} target="_blank" rel="noopener noreferrer" style={{marginLeft:8}}>Ouvrir</a>
            )}
            <span style={{marginLeft:8, color:'#888'}}>{file.type}</span>
            <span style={{marginLeft:8, color:'#aaa'}}>{file.created}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default UserFilesList;
