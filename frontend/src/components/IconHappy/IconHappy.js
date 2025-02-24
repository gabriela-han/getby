import React from 'react';
import styles from './IconHappy.module.css';
import iconHappy from '../../assets/IconeFeliz.svg';

const IconHappy = () => (
  <a href="/paginaDica" className={styles.aMudaPagina}>
    <div className={styles.divIconHappy} data-testid="IconHappy">
      <img src={iconHappy} className={styles.imgIconHappy} alt="Ícone de Login e Logout"/>
      <label className={styles.labelIconHappy}>Feliz</label>
    </div>
  </a>
);

IconHappy.propTypes = {};

IconHappy.defaultProps = {};

export default IconHappy;
