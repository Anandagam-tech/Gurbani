import React, { useEffect, useRef, useState, ReactNode } from 'react';
import { createRoot } from 'react-dom/client';
import { HashRouter as Router, Routes, Route, Link, useLocation, useParams, useNavigate } from 'react-router-dom';
import { BookOpen, Info, Home as HomeIcon, Search, ArrowRight, Star, Heart, ExternalLink, Menu, X, ChevronLeft, RefreshCw, FileText } from 'lucide-react';

// --- Scroll Reveal Component ---
const Reveal = ({ children, delay = 0, className = "" }: { children: ReactNode; delay?: number; className?: string }) => {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setTimeout(() => {
              if (ref.current) ref.current.classList.add('active');
            }, delay);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );

    if (ref.current) observer.observe(ref.current);

    return () => observer.disconnect();
  }, [delay]);

  return (
    <div ref={ref} className={`reveal ${className}`}>
      {children}
    </div>
  );
};

// --- Layout Components ---
const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const toggleMenu = () => setIsOpen(!isOpen);

  const navLinks = [
    { name: 'Home', path: '/', icon: <HomeIcon size={18} /> },
    { name: 'Angs', path: '/angs', icon: <BookOpen size={18} /> },
    { name: 'About', path: '/about', icon: <Info size={18} /> },
  ];

  return (
    <nav style={{
      position: 'fixed',
      top: 0,
      width: '100%',
      zIndex: 50,
      backdropFilter: 'blur(12px)',
      backgroundColor: 'rgba(3, 6, 32, 0.85)',
      borderBottom: '1px solid rgba(255,255,255,0.05)'
    }}>
      <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '80px' }}>
        <Link to="/" style={{ fontSize: '24px', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ color: '#fff' }}>Gyan</span>
        </Link>

        {/* Desktop Menu */}
        <div style={{ display: 'flex', gap: '32px' }} className="desktop-menu">
          {navLinks.map((link) => (
            <Link
              key={link.name}
              to={link.path}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontWeight: 500,
                color: location.pathname === link.path ? '#fff' : '#94a3b8',
                transition: 'color 0.2s'
              }}
            >
              {link.icon}
              {link.name}
            </Link>
          ))}
        </div>

        {/* Mobile Toggle */}
        <button 
          onClick={toggleMenu} 
          style={{ 
            background: 'none', 
            border: 'none', 
            color: 'white', 
            cursor: 'pointer',
            display: 'none' // Hidden by default, shown in CSS media query if we had one. 
          }}
          className="mobile-toggle"
        >
          {isOpen ? <X /> : <Menu />}
        </button>
      </div>
      
      {/* Mobile Menu inline style logic */}
      <style>{`
        @media (max-width: 768px) {
          .desktop-menu { display: none !important; }
          .mobile-toggle { display: block !important; }
        }
      `}</style>
      
      {isOpen && (
        <div style={{
          position: 'absolute',
          top: '80px',
          left: 0,
          width: '100%',
          backgroundColor: '#0B0E1B',
          borderBottom: '1px solid rgba(255,255,255,0.1)',
          padding: '20px'
        }}>
          {navLinks.map((link) => (
            <Link
              key={link.name}
              to={link.path}
              onClick={() => setIsOpen(false)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '16px 0',
                color: location.pathname === link.path ? '#fff' : '#94a3b8',
                fontSize: '18px'
              }}
            >
              {link.icon}
              {link.name}
            </Link>
          ))}
        </div>
      )}
    </nav>
  );
};

const Footer = () => (
  <footer style={{ borderTop: '1px solid rgba(255,255,255,0.05)', padding: '60px 0', marginTop: 'auto', backgroundColor: '#030620' }}>
    <div className="container">
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '20px' }}>
        <div style={{ fontSize: '24px', fontWeight: 'bold' }}>
          Gyan
        </div>
        <p style={{ color: '#94a3b8', textAlign: 'center', maxWidth: '500px' }}>
          Illuminating the path of spirituality through the divine wisdom of Sri Guru Granth Sahib Ji, powered by modern AI.
        </p>
        <p style={{ color: '#64748b', fontSize: '14px', marginTop: '20px' }}>
          © {new Date().getFullYear()} Gyan. All rights reserved.
        </p>
      </div>
    </div>
  </footer>
);

// --- Pages ---
const Home = () => {
  return (
    <div style={{ paddingTop: '80px' }}>
      {/* Hero Section */}
      <section style={{ minHeight: '90vh', display: 'flex', alignItems: 'center', position: 'relative', overflow: 'hidden' }}>
        <div className="glow-blob" style={{ top: '20%', left: '20%', opacity: 0.4 }}></div>
        <div className="glow-blob" style={{ bottom: '20%', right: '20%', background: 'radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, rgba(0, 0, 0, 0) 70%)', opacity: 0.4 }}></div>

        <div className="container" style={{ position: 'relative', zIndex: 1 }}>
          <div style={{ maxWidth: '800px', margin: '0 auto', textAlign: 'center' }}>
            <Reveal>
              <span style={{ 
                display: 'inline-block', 
                padding: '6px 16px', 
                borderRadius: '20px', 
                backgroundColor: 'rgba(126, 34, 206, 0.1)', 
                color: '#d8b4fe', 
                fontSize: '14px', 
                fontWeight: 600,
                marginBottom: '24px',
                border: '1px solid rgba(126, 34, 206, 0.2)'
              }}>
                Discover Divine Wisdom
              </span>
            </Reveal>
            
            <Reveal delay={100}>
              <h1 style={{ fontSize: 'clamp(40px, 8vw, 72px)', lineHeight: 1.1, fontWeight: 800, marginBottom: '24px' }}>
                Explore the Depths of <br />
                <span className="text-gradient">Guru Granth Sahib Ji</span>
              </h1>
            </Reveal>

            <Reveal delay={200}>
              <p style={{ fontSize: '20px', color: '#94a3b8', marginBottom: '40px', lineHeight: 1.6 }}>
                Daily meanings, spiritual interpretations, and practical life lessons generated to help you connect with Gurbani.
              </p>
            </Reveal>

            <Reveal delay={300}>
              <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
                <Link to="/angs" className="btn btn-primary">
                  Start Reading <ArrowRight size={18} style={{ marginLeft: '8px', verticalAlign: 'middle', display: 'inline-block' }} />
                </Link>
                <Link to="/about" className="btn btn-secondary">
                  Learn More
                </Link>
              </div>
            </Reveal>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section style={{ padding: '100px 0', backgroundColor: '#0B0E1B' }}>
        <div className="container">
          <Reveal>
            <div style={{ textAlign: 'center', marginBottom: '80px' }}>
              <h2 style={{ fontSize: '36px', fontWeight: 700, marginBottom: '16px' }}>Key Features</h2>
              <p style={{ color: '#94a3b8', fontSize: '18px' }}>Designed to enhance your understanding and experience.</p>
            </div>
          </Reveal>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '30px' }}>
            {[
              { title: 'Word-by-Word Meanings', desc: 'Detailed breakdown of each word in the Gurmukhi verse.', icon: <Search color="#a855f7" /> },
              { title: 'Spiritual Interpretation', desc: 'Deep dive into the spiritual message and essence of the Shabad.', icon: <Heart color="#ef4444" /> },
              { title: 'Daily Life Lessons', desc: 'Practical applications of the teachings in your everyday life.', icon: <Star color="#eab308" /> }
            ].map((feature, idx) => (
              <Reveal key={idx} delay={idx * 100}>
                <div style={{ 
                  padding: '40px', 
                  backgroundColor: 'rgba(255,255,255,0.03)', 
                  borderRadius: '16px', 
                  border: '1px solid rgba(255,255,255,0.05)',
                  height: '100%',
                  transition: 'transform 0.3s ease'
                }}>
                  <div style={{ 
                    width: '50px', 
                    height: '50px', 
                    backgroundColor: 'rgba(255,255,255,0.05)', 
                    borderRadius: '12px', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center',
                    marginBottom: '20px'
                  }}>
                    {feature.icon}
                  </div>
                  <h3 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '12px' }}>{feature.title}</h3>
                  <p style={{ color: '#94a3b8', lineHeight: 1.6 }}>{feature.desc}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

const Angs = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [lastAngDone, setLastAngDone] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 60;

  // Fetch the dynamic progress to see how many Angs are done
  useEffect(() => {
    setLoading(true);
    
    // First try fetching progress.json from root
    fetch('progress.json')
      .then(res => {
        if (!res.ok) throw new Error("Not found in root");
        return res.json();
      })
      .then(data => {
        if (data && typeof data.last_ang_done === 'number') {
            setLastAngDone(data.last_ang_done);
        }
        setLoading(false);
      })
      .catch(() => {
        // Fallback: try output/progress.json
        fetch('output/progress.json')
            .then(res => res.json())
            .then(data => {
                if (data && typeof data.last_ang_done === 'number') {
                    setLastAngDone(data.last_ang_done);
                }
                setLoading(false);
            })
            .catch(err => {
                console.warn("Could not load progress.json from root or output folder.", err);
                setLoading(false);
            });
      });
  }, []);

  // Generate the array of available Angs based on last_ang_done
  const availableAngs = Array.from({ length: lastAngDone }, (_, i) => ({
    number: i + 1,
    filename: `ang_${String(i + 1).padStart(4, '0')}.html`
  }));

  const filteredAngs = availableAngs.filter(ang => 
    ang.number.toString().includes(searchTerm)
  );

  const totalPages = Math.ceil(filteredAngs.length / itemsPerPage);
  const currentAngs = filteredAngs.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  return (
    <div style={{ paddingTop: '120px', paddingBottom: '100px', minHeight: '100vh' }}>
      <div className="container">
        <Reveal>
          <div style={{ textAlign: 'center', marginBottom: '60px' }}>
            <h1 style={{ fontSize: '48px', fontWeight: 700, marginBottom: '20px' }} className="text-gradient">
              Browse Angs
            </h1>
            <p style={{ color: '#94a3b8', fontSize: '18px', maxWidth: '600px', margin: '0 auto 40px auto' }}>
              Showing {lastAngDone} generated Angs out of 1430.
            </p>
            
            <div style={{ position: 'relative', maxWidth: '500px', margin: '0 auto' }}>
              <input
                type="text"
                placeholder="Search available Angs..."
                value={searchTerm}
                onChange={handleSearch}
                style={{
                  width: '100%',
                  padding: '16px 24px',
                  borderRadius: '12px',
                  backgroundColor: 'rgba(255,255,255,0.05)',
                  border: '1px solid rgba(255,255,255,0.1)',
                  color: 'white',
                  fontSize: '16px',
                  outline: 'none',
                  transition: 'all 0.3s'
                }}
                onFocus={(e) => e.target.style.borderColor = '#a855f7'}
                onBlur={(e) => e.target.style.borderColor = 'rgba(255,255,255,0.1)'}
              />
              <Search style={{ position: 'absolute', right: '20px', top: '50%', transform: 'translateY(-50%)', color: '#94a3b8' }} />
            </div>
          </div>
        </Reveal>

        {loading ? (
           <div style={{ textAlign: 'center', padding: '60px', color: '#a855f7' }}>
             Loading progress...
           </div>
        ) : filteredAngs.length > 0 ? (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))', gap: '16px' }}>
              {currentAngs.map((ang) => (
                <Reveal key={ang.number} delay={0}>
                  <Link 
                    to={`/ang/${ang.number}`}
                    style={{ 
                      display: 'flex', 
                      flexDirection: 'column',
                      alignItems: 'center', 
                      justifyContent: 'center',
                      padding: '20px', 
                      backgroundColor: 'rgba(30, 41, 59, 0.4)', 
                      borderRadius: '12px',
                      border: '1px solid rgba(255,255,255,0.05)',
                      transition: 'all 0.2s',
                      textDecoration: 'none',
                      cursor: 'pointer'
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.transform = 'translateY(-4px)';
                      e.currentTarget.style.backgroundColor = 'rgba(126, 34, 206, 0.2)';
                      e.currentTarget.style.borderColor = '#a855f7';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.transform = 'translateY(0)';
                      e.currentTarget.style.backgroundColor = 'rgba(30, 41, 59, 0.4)';
                      e.currentTarget.style.borderColor = 'rgba(255,255,255,0.05)';
                    }}
                  >
                    <span style={{ fontSize: '14px', color: '#94a3b8', marginBottom: '4px' }}>Ang</span>
                    <span style={{ fontSize: '24px', fontWeight: 700, color: 'white' }}>{ang.number}</span>
                  </Link>
                </Reveal>
              ))}
            </div>
        ) : (
            <div style={{ textAlign: 'center', padding: '60px', color: '#94a3b8', backgroundColor: 'rgba(255,255,255,0.03)', borderRadius: '16px' }}>
              <FileText size={40} style={{ marginBottom: '16px', opacity: 0.5 }} />
              <h3>No Angs Found</h3>
              <p>Based on your <code>progress.json</code>, no Angs have been generated yet.</p>
              <p style={{ fontSize: '14px', marginTop: '10px', opacity: 0.7 }}>
                  Run your Python script to generate content, then refresh this page.
              </p>
            </div>
        )}

        {/* Pagination */}
        {totalPages > 1 && (
          <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', marginTop: '60px' }}>
            <button 
              onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
              disabled={currentPage === 1}
              className="btn btn-secondary"
              style={{ padding: '8px 16px', opacity: currentPage === 1 ? 0.5 : 1 }}
            >
              Previous
            </button>
            <span style={{ display: 'flex', alignItems: 'center', color: '#94a3b8' }}>
              Page {currentPage} of {totalPages}
            </span>
            <button 
              onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
              className="btn btn-secondary"
              style={{ padding: '8px 16px', opacity: currentPage === totalPages ? 0.5 : 1 }}
            >
              Next
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

// --- Viewer Component ---
const AngViewer = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [htmlContent, setHtmlContent] = useState('');
  
  const angNumber = parseInt(id || "1");
  const filename = `output/ang_${String(angNumber).padStart(4, '0')}.html`;

  useEffect(() => {
    setLoading(true);
    setError(false);
    setHtmlContent('');
    
    // Fetch and parse HTML to inject directly into the page
    // This allows the content to share the main window scrollbar
    fetch(filename)
      .then(res => {
        if (!res.ok) throw new Error("Not found");
        return res.text();
      })
      .then(text => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, 'text/html');
        // Extract innerHTML from body to inject
        setHtmlContent(doc.body.innerHTML);
        setLoading(false);
      })
      .catch(() => {
        setError(true);
        setLoading(false);
      });
  }, [filename]);

  return (
    <div style={{ paddingTop: '80px', minHeight: '100vh', display: 'flex', flexDirection: 'column', backgroundColor: '#0B0E1B' }}>
        <div style={{ 
          padding: '10px 20px', 
          backgroundColor: 'rgba(3, 6, 32, 0.95)', 
          borderBottom: '1px solid rgba(255,255,255,0.05)', 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'space-between',
          height: '60px',
          position: 'sticky',
          top: '80px',
          zIndex: 40
        }}>
             <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
               <button onClick={() => navigate('/angs')} className="btn btn-secondary" style={{ padding: '6px 12px', fontSize: '14px', display: 'flex', alignItems: 'center', gap: '6px', borderRadius: '8px' }}>
                  <ChevronLeft size={16} /> Back
               </button>
               <span style={{color: 'white', fontWeight: 600}}>Ang {angNumber}</span>
             </div>
             
             <div style={{ display: 'flex', gap: '8px' }}>
               <button 
                 onClick={() => navigate(`/ang/${Math.max(1, angNumber - 1)}`)} 
                 disabled={angNumber <= 1}
                 className="btn btn-secondary" 
                 style={{ padding: '6px 12px', fontSize: '14px', borderRadius: '8px', opacity: angNumber <= 1 ? 0.5 : 1 }}
               >
                 Prev
               </button>
               <button 
                 onClick={() => navigate(`/ang/${Math.min(1430, angNumber + 1)}`)} 
                 disabled={angNumber >= 1430}
                 className="btn btn-secondary" 
                 style={{ padding: '6px 12px', fontSize: '14px', borderRadius: '8px', opacity: angNumber >= 1430 ? 0.5 : 1 }}
               >
                 Next
               </button>
             </div>
        </div>
        
        {loading ? (
            <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '50vh' }}>
                <div style={{ color: '#a855f7' }}>Loading Content...</div>
            </div>
        ) : error ? (
            <div className="container" style={{ textAlign: 'center', marginTop: '100px' }}>
                 <div style={{ display: 'inline-flex', padding: '20px', borderRadius: '50%', backgroundColor: 'rgba(239, 68, 68, 0.1)', marginBottom: '20px' }}>
                    <ExternalLink size={40} color="#ef4444" />
                 </div>
                 <h2 style={{fontSize: '24px', marginBottom: '16px'}}>Ang {angNumber} Not Found</h2>
                 <p style={{color: '#94a3b8', marginBottom: '30px', maxWidth: '500px', margin: '0 auto 30px auto', lineHeight: 1.6}}>
                    The output file <code>{filename}</code> could not be loaded. 
                    <br/><br/>
                    Please ensure the file exists and your Python script has run successfully for this Ang.
                 </p>
                 <button onClick={() => navigate('/angs')} className="btn btn-primary">Return to Angs List</button>
            </div>
        ) : (
             // Inject content directly to allow main window scrolling
             <div 
                className="ang-content-wrapper"
                style={{ flex: 1, width: '100%' }}
                dangerouslySetInnerHTML={{ __html: htmlContent }} 
             />
        )}
    </div>
  );
}

const About = () => {
  return (
    <div style={{ paddingTop: '120px', paddingBottom: '100px', minHeight: '100vh' }}>
      <div className="container" style={{ maxWidth: '800px' }}>
        <Reveal>
          <h1 style={{ fontSize: '48px', fontWeight: 700, marginBottom: '40px', textAlign: 'center' }} className="text-gradient">
            About This Project
          </h1>
        </Reveal>

        <Reveal delay={100}>
          <div style={{ 
            backgroundColor: '#0B0E1B', 
            padding: '40px', 
            borderRadius: '24px', 
            border: '1px solid rgba(255,255,255,0.05)',
            marginBottom: '40px'
          }}>
            <h2 style={{ fontSize: '24px', color: 'white', marginBottom: '20px' }}>Mission</h2>
            <p style={{ color: '#94a3b8', lineHeight: 1.8, marginBottom: '20px' }}>
              This project aims to bridge the gap between ancient wisdom and modern understanding. By leveraging advanced AI technology, we generate detailed word-by-word meanings, spiritual interpretations, and practical life lessons for each Ang of Sri Guru Granth Sahib Ji.
            </p>
            <p style={{ color: '#94a3b8', lineHeight: 1.8 }}>
              Inspired by the teachings of Sikh scholars, the goal is to make Gurbani accessible to everyone, regardless of their proficiency in Gurmukhi or Punjabi.
            </p>
          </div>
        </Reveal>

        <Reveal delay={200}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div style={{ 
              backgroundColor: 'rgba(255,255,255,0.03)', 
              padding: '30px', 
              borderRadius: '16px',
              border: '1px solid rgba(255,255,255,0.05)'
            }}>
              <h3 style={{ fontSize: '18px', color: '#a855f7', marginBottom: '10px' }}>How it Works</h3>
              <p style={{ color: '#94a3b8', fontSize: '14px', lineHeight: 1.6 }}>
                A Python script extracts Gurbani data from the BaniDB API, processes it through a local LLM (Ollama), and generates comprehensive HTML pages which are hosted here.
              </p>
            </div>
            
            <div style={{ 
              backgroundColor: 'rgba(255,255,255,0.03)', 
              padding: '30px', 
              borderRadius: '16px',
              border: '1px solid rgba(255,255,255,0.05)'
            }}>
              <h3 style={{ fontSize: '18px', color: '#3b82f6', marginBottom: '10px' }}>Open Source</h3>
              <p style={{ color: '#94a3b8', fontSize: '14px', lineHeight: 1.6 }}>
                This project is built with transparency and community in mind. The output is statically generated for speed and reliability.
              </p>
            </div>
          </div>
        </Reveal>
      </div>
    </div>
  );
};

// --- App Component ---
const App = () => {
  return (
    <Router>
      <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/angs" element={<Angs />} />
          <Route path="/ang/:id" element={<AngViewer />} />
          <Route path="/about" element={<About />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
};

const root = createRoot(document.getElementById('root')!);
root.render(<App />);
