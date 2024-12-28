import React from 'react'
import styles from '../components/Footer.module.css'
const Footer = () => {
  const date = new Date();
  return (
    <div className={styles.mainContainer}>
      <hr></hr>
      <div>
      <p> &reg;Devolopers:  <li>1.<a href='https://github.com/Kowsar21' className={styles.Link} target='_blank'>Kowsar</a></li>
                            <li>2.<a href='https://www.facebook.com/jsd.saikat.dhrobo' className={styles.Link} target='_blank'>Saikat</a></li>
                          <li>3.<a href='https://www.facebook.com/fahim.mahmud.3114' className={styles.Link} target='_blank'>Fahim</a></li>
                            <li>4.<a href='https://www.facebook.com/md.al.amin.islam.siam.2024' className={styles.Link} target='_blank'>Al-amin</a></li>
       </p> 
      </div>

    </div>
  );
}

export default Footer;