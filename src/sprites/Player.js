import Phaser from 'phaser'

export default class extends Phaser.Sprite {
  constructor ({ game, x, y }) {
    super(game, x, y, 'player');

    const fps = 10;
    this.animations.add('walk', [0,1,2,3,4,5,6,7], fps, true);
    this.animations.add('stand', [8], fps, false);

    this.animations.play('walk');
    this.animations.play('stand');

    this.anchor.setTo(0.5);
  }

  update () {
    //this.scale.x = -1;
  }
}
