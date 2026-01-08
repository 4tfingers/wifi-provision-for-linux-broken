const { useState, useEffect } = React;

function SimpleWifiForm() {
    const [ssid, setSsid] = useState("");
    const [password, setPassword] = useState("");
    const [status, setStatus] = useState("");

    useEffect(() => {
        // Add CSS animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            @keyframes slideIn {
                0% { opacity: 0; transform: translateY(-10px); }
                100% { opacity: 1; transform: translateY(0); }
            }
            @keyframes fadeIn {
                0% { opacity: 0; transform: translateY(20px); }
                100% { opacity: 1; transform: translateY(0); }
            }
        `;
        document.head.appendChild(style);
        return () => document.head.removeChild(style);
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!ssid || !password) {
            setStatus("error");
            return;
        }

        setStatus("connecting");
        
        // Send to device endpoint
        try {
            await fetch('/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ essid, password })
            });
            setStatus("success");
        } catch {
            setStatus("error");
        }
    };

    return (
        <div style={{ 
            textAlign: 'center',
            animation: 'fadeIn 1s ease-out'
        }}>
            <div style={{
                marginBottom: '24px'
            }}>
                <h1 style={{ display: 'flex', 
					flexDirection: 'column', 
					gap: '24px',
                    fontSize: '36px',
                    fontWeight: '700',
                    color: '#e2e8f0',
                    margin: '0 0 12px 0',
                    letterSpacing: '-0.02em'
                }}>
                   A Flask HTTP WiFi Connector
                </h1>
            </div>

            <div style={{
                maxWidth: '440px',
                margin: '0 auto',
                padding: '40px',
                background: 'rgba(57, 79, 116, 1)',
                backdropFilter: 'blur(10px)',
                borderRadius: '24px',
                boxShadow: 'none',
                border: '1px solid rgba(148, 163, 184, 0.2)',
                fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, sans-serif'
            }}>
                <div style={{ textAlign: 'center', marginBottom: '32px' }}>
                    <div style={{
                        background: 'rgba(57, 79, 116, 1)',
                        backdropFilter: 'blur(10px)',
                        padding: '10px',
                        borderRadius: '1px',
                        display: 'inline-block',
                        marginBottom: '10px',
                        boxShadow: 'none',
                        border: 'none'
                    }}>
                        <img 
                            src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/800px-Tux.svg.png"
                            alt="raspberrypi"
                            style={{
                                height: '100px',
                                width: 'auto'
                            }}
                        />
                    </div>
                    <h2 style={{ display: 'flex', 
						flexDirection: 'column', 
						gap: '24px',
                        margin: '0 0 8px 0', 
                        fontSize: '24px', 
                        fontWeight: '600',
                        color: '#e2e8f0',
                        letterSpacing: '-0.01em'
                    }}>
                        WiFi Setup
                    </h2>
                    <p style={{ 
                        margin: 0, 
                        fontSize: '15px', 
                        color: '#94a3b8',
                        fontWeight: '400'
                    }}>
                        Enter your WiFi credentials to connect your device to the network
                    </p>
                </div>
                
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
					<div>
						<label style={{
							display: 'block',
							marginBottom: '8px',
							fontSize: '14px',
							fontWeight: '600',
							color: '#e2e8f0',
							textAlign: 'left'
						}}>
							SSID Selector
						</label>
						<select
								onChange=
								style={{}}
						>
						</select>		
					</div>		
                    <div>
                        <label style={{
                            display: 'block',
                            marginBottom: '8px',
                            fontSize: '14px',
                            fontWeight: '600',
                            color: '#e2e8f0',
                            textAlign: 'left'
                        }}>
                            Network Name (SSID)
                        </label>
                        <input
                            type="text"
                            placeholder="Enter WiFi network name"
                            value={ssid} // why ssid when parsed essid
                            onChange={(e) => setSsid(e.target.value)}
                            style={{
                                width: '100%',
                                padding: '16px 20px',
                                border: '2px solid rgba(148, 163, 184, 0.2)',
                                borderRadius: '12px',
                                fontSize: '16px',
                                fontFamily: 'inherit',
                                boxSizing: 'border-box',
                                background: 'rgba(15, 23, 42, 0.6)',
                                color: '#f1f5f9',
                                transition: 'all 0.2s ease',
                                outline: 'none'
                            }}
                            onFocus={(e) => {
                                e.target.style.borderColor = '#3b82f6';
                                e.target.style.background = 'rgba(15, 23, 42, 0.8)';
                            }}
                            onBlur={(e) => {
                                e.target.style.borderColor = 'rgba(148, 163, 184, 0.2)';
                                e.target.style.background = 'rgba(15, 23, 42, 0.6)';
                            }}
                        />
                    </div>
                    
                    <div>
                        <label style={{
                            display: 'block',
                            marginBottom: '8px',
                            fontSize: '14px',
                            fontWeight: '600',
                            color: '#e2e8f0',
                            textAlign: 'left'
                        }}>
                            Password
                        </label>
                        <div style={{ position: 'relative' }}>
                            <span style={{
                                position: 'absolute',
                                left: '20px',
                                top: '50%',
                                transform: 'translateY(-50%)',
                                color: '#64748b',
                                fontSize: '18px'
                            }}>🔒</span>
                            <input
                                type="password"
                                placeholder="Enter WiFi password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                style={{
                                    width: '100%',
                                    padding: '16px 20px 16px 50px',
                                    border: '2px solid rgba(148, 163, 184, 0.2)',
                                    borderRadius: '12px',
                                    fontSize: '16px',
                                    fontFamily: 'inherit',
                                    boxSizing: 'border-box',
                                    background: 'rgba(15, 23, 42, 0.6)',
                                    color: '#f1f5f9',
                                    transition: 'all 0.2s ease',
                                    outline: 'none'
                                }}
                                onFocus={(e) => {
                                    e.target.style.borderColor = '#3b82f6';
                                    e.target.style.background = 'rgba(15, 23, 42, 0.8)';
                                }}
                                onBlur={(e) => {
                                    e.target.style.borderColor = 'rgba(148, 163, 184, 0.2)';
                                    e.target.style.background = 'rgba(15, 23, 42, 0.6)';
                                }}
                            />
                        </div>
                    </div>
                    
                    <button
                        type="submit"
                        disabled={!ssid || !password || status === 'connecting'}
                        style={{
                            width: '100%',
                            padding: '18px 24px',
                            background: status === 'success' 
                                ? 'linear-gradient(135deg, #10b981, #059669)' 
                                : 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
                            color: 'white',
                            border: 'none',
                            borderRadius: '12px',
                            fontSize: '16px',
                            fontWeight: '600',
                            fontFamily: 'inherit',
                            cursor: (!ssid || !password || status === 'connecting') ? 'not-allowed' : 'pointer',
                            opacity: (!ssid || !password || status === 'connecting') ? 0.5 : 1,
                            transition: 'all 0.3s ease',
                            boxShadow: '0 8px 25px rgba(59, 130, 246, 0.3)',
                            transform: 'translateY(0)',
                            outline: 'none',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            gap: '8px'
                        }}
                        onMouseEnter={(e) => {
                            if (!e.target.disabled) {
                                e.target.style.transform = 'translateY(-2px)';
                                e.target.style.boxShadow = '0 12px 35px rgba(59, 130, 246, 0.4)';
                            }
                        }}
                        onMouseLeave={(e) => {
                            e.target.style.transform = 'translateY(0)';
                            e.target.style.boxShadow = '0 8px 25px rgba(59, 130, 246, 0.3)';
                        }}
                    >
                        {status === 'connecting' ? (
                            <>
                                <div style={{
                                    width: '16px',
                                    height: '16px',
                                    border: '2px solid rgba(255,255,255,0.3)',
                                    borderTop: '2px solid white',
                                    borderRadius: '50%',
                                    animation: 'spin 1s linear infinite'
                                }}></div>
                                Connecting...
                            </>
                        ) : status === 'success' ? (
                            <>
                                <span>✓</span>
                                Connected!
                            </>
                        ) : (
                            <>
                                <span>📶</span>
                                Connect to Network
                            </>
                        )}
                    </button>
                    
                    {status === 'success' && (
                        <div style={{ 
                            padding: '16px', 
                            background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1))',
                            color: '#34d399',
                            borderRadius: '12px',
                            fontSize: '14px',
                            textAlign: 'center',
                            fontWeight: '500',
                            border: '1px solid rgba(52, 211, 153, 0.3)',
                            animation: 'slideIn 0.3s ease'
                        }}>
                            🎉 Successfully connected to "{ssid}"
                        </div>
                    )}
                    
                    {status === 'error' && (
                        <div style={{ 
                            padding: '16px', 
                            background: 'linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.1))',
                            color: '#f87171',
                            borderRadius: '12px',
                            fontSize: '14px',
                            textAlign: 'center',
                            fontWeight: '500',
                            border: '1px solid rgba(248, 113, 113, 0.3)',
                            animation: 'slideIn 0.3s ease'
                        }}>
                            ⚠️ Connection failed. Please check your credentials and try again.
                        </div>
                    )}
                </form>
            </div>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<SimpleWifiForm />);
