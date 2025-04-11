import styles from './Button.module.css';
import PropTypes from 'prop-types';

export function Button({outline, children, className, size="large", ...others}) {
    return (
        <button {...others} 
        className={`${styles.button} ${styles[size]} ${outline ? styles.outline : ""} ${className}`}> 
            {children} 
        </button>
    )
}


Button.propTypes = {
    outline: PropTypes.bool
};