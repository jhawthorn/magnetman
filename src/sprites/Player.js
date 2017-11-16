import Phaser from 'phaser'

export default class extends Phaser.Sprite {
  constructor ({ game, x, y }) {
    super(game, x, y, 'player');

    game.physics.enable(this, Phaser.Physics.ARCADE);

    this.body.collideWorldBounds = true;
    this.body.gravity.y = 500;
    this.body.maxVelocity.y = 300;
    this.body.maxVelocity.x = 150;
    this.body.linearDamping = 1;
    this.body.setSize(20, 26, 0, 0);

    const fps = 15;
    this.animations.add('walk', [0,1,2,3,4,5,6,7], fps, true);
    this.animations.add('stand', [8]);
    this.animations.add('jump', [11]);

    this.animations.play('walk');

    this.anchor.setTo(0.5, 1);

    this.cursors = game.input.keyboard.createCursorKeys();
    this.jumpButton = game.input.keyboard.addKey(Phaser.Keyboard.Z);
  }

  update () {
    if (this.cursors.left.isDown) {
      this.body.velocity.x -= this.body.onFloor() ? 50 : 25;
      this.animations.play('walk');
      this.scale.x = 1;
    } else if (this.cursors.right.isDown) {
      this.body.velocity.x += this.body.onFloor() ? 50 : 25;
      this.animations.play('walk');
      this.scale.x = -1;
    } else {
      this.animations.play('stand');
    }

    if (this.jumpButton.isDown && this.body.onFloor()) {
      this.body.velocity.y = -500;
    }

    if (this.body.onFloor()) {
      this.body.drag.x = 800;
    } else {
      this.body.drag.x = 100;
      this.animations.play('jump');
    }
  }
}
