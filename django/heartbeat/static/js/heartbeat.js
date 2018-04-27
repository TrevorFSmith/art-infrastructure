(function () {

  'use strict'

  class Hello extends React.Component {
    render() {
      return React.createElement('div', null, `${this.props.toWhat} mounted.`);
    }
  }

  ReactDOM.render(
    React.createElement(Hello, {toWhat: 'React'}, null),
    document.getElementById('root')
  );

}());
