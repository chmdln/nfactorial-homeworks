import styles from './Input.module.css';
import PropTypes from 'prop-types';

export function Input({ label, size, width, ...others }) {
    return (
        <div className={`${styles.root} ${styles[size || "large"]}`}>
            <label>{label}</label>
            <input {...others} 
            style={{
                width: width ? `${width}px` : '100%'
            }}>
            </input>       
        </div>
    );
  }
  
// PropTypes for type checking
Input.propTypes = {
    label: PropTypes.string
};  