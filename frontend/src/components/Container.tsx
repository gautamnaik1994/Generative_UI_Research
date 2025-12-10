// Generate code for Container component

import React from 'react'

interface ContainerProps {
  children?: React.ReactNode
  variant?: 'fluid' | 'fixed'
  direction?: 'row' | 'column'
}

const Container: React.FC<ContainerProps> = ({
  children,
  variant = 'fixed',
  direction = 'row',
}) => {
  return <div className={`container ${variant} ${direction}`}>{children}</div>
}

export default Container
